#!/usr/bin/python3

import argparse
import itertools
import pathlib
import time
import json
from pprint import pprint, pformat
from collections import deque
from datetime import timedelta, datetime
from typing import Tuple, Callable

import requests
from loguru import logger


from PushMethod import modules


ROOT = pathlib.Path(__file__).parent.absolute()


def get_new_token(client_id, client_secret) -> Tuple[str, int]:
    url = "https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials&scope="

    formatted = url.format(client_id, client_secret)
    logger.debug(formatted)

    req = requests.post(formatted)

    dict_ = req.json()

    token = dict_["access_token"]
    expires_in = dict_["expires_in"]

    return token, expires_in


class RequestInstance:
    def __init__(self, channel_name, client_id, client_secret, callback: Callable):
        self.client_id = client_id
        self.client_secret = client_secret

        self.channel_name = channel_name
        self.header = {}
        self.next_check = time.time()

        self.cached = deque(maxlen=5)

        self.generate_new_header()

        self.callback = callback

    def generate_new_header(self):
        token, eta = get_new_token(self.client_id, self.client_secret)

        next_checkup = datetime.now() + timedelta(seconds=round(eta))

        header = {
            "Authorization": f"Bearer {token}",
            "Client-ID": f"{self.client_id}"
        }

        logger.info("Got token [{}]. Will expire in {}", token, (next_checkup - datetime.now()).total_seconds())

        self.header = header
        self.next_check = next_checkup.timestamp()

    def exact_match(self, response):

        for dict_ in response.json()["data"]:
            if dict_["broadcaster_login"] == self.channel_name:
                return dict_

        logger.warning("Could not find exact match of user {}", self.channel_name)
        return None

    def start_checking(self):
        request_url = f"https://api.twitch.tv/helix/search/channels?query={self.channel_name}"
        # user_id_query = f"https://api.twitch.tv/helix/users?&id={self.channel_name}"

        with requests.session() as session:

            # get user ID
            req = session.get(request_url, headers=self.header)

            while True:
                while time.time() < self.next_check:
                    req = session.get(request_url, headers=self.header)

                    logger.debug("response: {}", req)
                    matched = self.exact_match(req)
                    logger.debug("Found matching: \n{}", pformat(matched, indent=2))

                    if matched["is_live"] and matched["started_at"] not in self.cached:
                        self.cached.append(matched["started_at"])
                        logger.info("Found an active live stream for channel {}", self.channel_name)

                        self.callback(f"\nhttps://twitch.tv/{self.channel_name}")

                    logger.debug("Rate left: {} Date: {}", req.headers["Ratelimit-Remaining"], req.headers["Date"])

                    time.sleep(5)

                # Get new token
                self.generate_new_header()


def callback_notify_closure(notify_callbacks):

    def inner(content="test run"):
        logger.info("Notifier callback started.")
        for callback in notify_callbacks:
            callback(content)

    return inner


def main():

    config = json.loads(args.path.read_text(encoding="utf8"))

    channel_name = config["channel name"]
    client_id = config["polling api"]["twitch app id"]
    client_secret = config["polling api"]["twitch app secret"]

    logger.info("Target Channel: {}", channel_name)

    callback_list = []

    # verify
    for method in modules:
        if method.verify(config):
            callback_list.append(method.send_closure(config))

    callback_unified = callback_notify_closure(callback_list)

    req_instance = RequestInstance(channel_name, client_id, client_secret, callback_unified)

    req_instance.start_checking()


if __name__ == "__main__":

    # parsing start =================================

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--path",
        metavar="CONFIG_PATH",
        type=pathlib.Path,
        default=ROOT.joinpath("configuration.json"),
        help="Path to configuration json file. Default path is 'configuration.json' adjacent to this script",
    )
    args = parser.parse_args()

    # parsing end ===================================

    main()

#!/usr/bin/python3

import traceback
import argparse
import pathlib
import time
import json
from typing import Callable

from loguru import logger


from PushMethod import modules
from twitch_api_client import TwitchClient


ROOT = pathlib.Path(__file__).parent.absolute()
USE_GET_STREAM = True


class Notified:
    def __init__(self):
        self.file = args.cache
        self.last_notified = self.file.read_text("utf8") if self.file.exists() else ""

    def write(self, new_time):
        self.last_notified = new_time
        self.file.write_text(new_time, "utf8")

    def __contains__(self, item):
        return item == self.last_notified


class RequestInstance:
    def __init__(self, client: TwitchClient, channel_name, callback: Callable):

        self.notified = Notified()

        self.client = client

        self.channel_name = channel_name

        self.callback = callback

    def start_checking(self):

        user = self.client.get_user(self.channel_name)

        logger.info("Found user: {}", user)

        if USE_GET_STREAM:
            logger.info("Started listening using GET_STREAM.")
            while True:
                output = self.client.get_stream(user.id, log=False)

                if output and output.type == "live" and output.started_at not in self.notified:
                    logger.info("Found an active live stream for channel {}", self.channel_name)

                    self.notified.write(output.started_at)
                    self.callback(f"\nhttps://twitch.tv/{self.channel_name}", output)

                time.sleep(2)

        else:
            while True:
                output = self.client.search_channel(user.login)

                if output.is_live and output.started_at not in self.notified:
                    logger.info("Found an active live stream for channel {}", self.channel_name)

                    self.notified.write(output.started_at)
                    self.callback(f"\nhttps://twitch.tv/{self.channel_name}", output)

                time.sleep(2)


def callback_notify_closure(notify_callbacks):

    def inner(content, channel_object):
        logger.info("Notifier callback started.")
        for callback in notify_callbacks:
            try:
                callback.send(content, channel_object)
            except Exception:
                traceback.print_exc()

    return inner


def main():

    config = json.loads(args.path.read_text(encoding="utf8"))

    channel_name = config["channel name"]
    client_id = config["polling api"]["twitch app id"]
    client_secret = config["polling api"]["twitch app secret"]

    client = TwitchClient(client_id, client_secret)

    logger.info("Target Channel: {}", channel_name)

    callback_list = []

    # verify
    for method in modules:
        try:
            instance = method(config["push methods"])
        except Exception:

            logger.warning("Got Error initializing {}", method.__name__)
            traceback.print_exc()
        else:
            callback_list.append(instance)

    callback_unified = callback_notify_closure(callback_list)

    req_instance = RequestInstance(client, channel_name, callback_unified)

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
    parser.add_argument(
        "-c",
        "--cache",
        metavar="CACHE_PATH",
        type=pathlib.Path,
        default=ROOT.joinpath("cache.json"),
        help="Path where cache file will be. Default path is 'cache.json' adjacent to this script",
    )
    args = parser.parse_args()

    args.cache.touch(exist_ok=True)

    # parsing end ===================================

    main()

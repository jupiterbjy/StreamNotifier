#!/usr/bin/python3

import time
import traceback
import argparse
import pathlib
import json
from typing import Callable

from loguru import logger

from PushMethod import modules
from youtube_api_client import build_client, YoutubeClient, LiveBroadcast


ROOT = pathlib.Path(__file__).parent.absolute()
TOKEN_PATH = ROOT.joinpath("token.json")
LOCAL_TESTING = False
INTERVAL = 10


class Notified:
    def __init__(self):
        self.file = args.cache
        self.last_notified = self.file.read_text("utf8") if self.file.exists() else ""

    def write(self, new_id):
        self.last_notified = new_id
        self.file.write_text(new_id, "utf8")

    def __contains__(self, item):
        return item == self.last_notified


def callback_notify_closure(notify_callbacks):
    test = args.test

    if test:
        logger.warning("Test mode enabled, will not push to platforms")

    def inner(channel_object: LiveBroadcast):
        logger.info("Notifier callback started for stream {}", channel_object)
        for callback in notify_callbacks:

            if test:
                logger.info("Test mod, skipping {}", type(callback).__name__)
                continue
            else:
                logger.info("Pushing for {}", type(callback).__name__)

            try:
                callback.send(channel_object)
            except Exception:
                traceback.print_exc()

    return inner


def start_checking(client: YoutubeClient, callback: Callable, interval):
    notified = Notified()

    logger.info("Started polling for streams, interval: {}", interval)

    while True:
        try:
            active = client.get_active_user_broadcasts(max_results=1)
        except Exception:
            traceback.print_exc()
        else:
            if active and active[0].id not in notified:
                # gotcha! there's active stream
                stream = active[0]

                logger.debug("Received: {}", stream)

                # write in cache and
                notified.write(stream.id)
                callback(stream)

        time.sleep(interval)


def main():

    # read config meow
    config = json.loads(args.path.read_text(encoding="utf8"))
    client_secret_dir = config["client secret file path"]

    client = build_client(client_secret_dir=client_secret_dir, token_dir=TOKEN_PATH, console=not LOCAL_TESTING)

    logger.info("Application successfully authorized.")

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

    start_checking(client, callback_unified, INTERVAL)


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
    parser.add_argument(
        "-t",
        "--test",
        action="store_true",
        default=False,
        help="Enable test mode, this does not actually push to platforms.",
    )
    args = parser.parse_args()

    args.cache.touch(exist_ok=True)

    # parsing end ===================================

    main()

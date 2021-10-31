#!/usr/bin/python3

import time
import traceback
import argparse
import pathlib
import json
from typing import Callable, Union

from loguru import logger

from PushMethod import available_methods
from discord_report import report_closure



ROOT = pathlib.Path(__file__).parent.absolute()


class NameSpace:
    def __init__(self):
        # self.test_mode: Union[bool, None] = None
        self.path: Union[pathlib.Path, None] = None
        # self.cache_path: Union[pathlib.Path, None] = None



def main():

    # read config meow
    config = json.loads(args.path.read_text(encoding="utf8"))
    client_secret_dir = config["client_secret_path"]
    config["cache_path"] = pathlib.Path(config["cache_path"])

    report = report_closure(config)

    client = build_client(client_secret_dir=client_secret_dir, token_dir=TOKEN_PATH, console=not LOCAL_TESTING)

    logger.info("Application successfully authorized.")

    callback_list = list(available_methods(config))
    names = tuple(x.__class__.__name__ for x in callback_list)

    logger.info("Verified {}", ", ".join(names))

    callback_unified = callback_notify_closure(callback_list)

    report(title="Notifier Started", fields={
        "Active Push Destination": "\n".join(names)
    })


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
    # parser.add_argument(
    #     "-c",
    #     "--cache",
    #     metavar="CACHE_PATH",
    #     type=pathlib.Path,
    #     default=ROOT.joinpath("cache.json"),
    #     help="Path where cache file will be. Default path is 'cache' adjacent to this script",
    # )
    # parser.add_argument(
    #     "-t",
    #     "--test",
    #     action="store_true",
    #     default=False,
    #     help="Enable test mode, this does not actually push to platforms.",
    # )

    args = NameSpace()
    parser.parse_args(namespace=args)

    # parsing end ===================================

    main()

"""Youtube stream checker
"""

from typing import Callable
import traceback
import time

from loguru import logger
from googleapiclient.errors import HttpError
import trio

from youtube_api_client import build_client
from .base import StreamIdCache


class YoutubeStreamCheck:
    notify_config = {
        "username": "Youtube Notifier",
        "icon": "https://imgur.com/tDOQPK9.png",
        "color": "ff0000"
    }

    def __init__(self, config: dict, notifier_class, report_instance):
        """
        Args:
            config: source.youtube config
        """
        # not really needed, just to make linter happy

        self.config = config
        self.cache = StreamIdCache(config["cache_path"])
        self.notifier = notifier_class(self.config)
        self.report = report_instance
        self.interval = config["interval"]

        self.client = build_client(client_secret_dir=config["client_secret_path"], token_dir=config["token_path"], console=True)

        self.last_err = ""
        self.ignore_http_500 = self.config["suppress_http_500"]

    async def wait_for_stream(self):

        logger.info("Started polling for streams, interval: {}", self.interval)

        last_err = ""

        while True:

            await trio.sleep(self.interval)

            try:
                active = self.client.get_active_user_broadcasts(max_results=1)

            except Exception as err:
                # ignore 500 internal server error according to configuration
                if self.ignore_http_500 and isinstance(err, HttpError) and err.status_code == 500:
                    logger.info("Suppressing http 500 error")
                    continue

                msg = str(err)

                if last_err == msg:
                    logger.critical("Previous Exception still in effect")
                else:
                    last_err = msg
                    traceback.print_exc(limit=4)
                    self.report(title="Youtube Notifier Down", desc=traceback.format_exc(limit=4))

            else:
                if last_err:
                    last_err = ""
                    self.report(title="Youtube Notifier Up", desc="Last exception cleared")

                if active and active[0].id not in self.cache:
                    # gotcha! there's active stream
                    stream = active[0]

                    logger.debug("Found Active stream: {}", stream)

                    self.report(title="Stream Found", desc="Private Streams will not be pushed.", fields={
                        "Started": stream.actual_start_time,
                        "Title": stream.title,
                        "Privacy": stream.privacy_status,
                        "link": stream.link,
                        "Live": stream.life_cycle_status
                    })
                    # write in cache and notify if not private
                    self.cache.write(stream.id)

                    if stream.privacy_status != "private":
                        self.notifier.notify(stream)

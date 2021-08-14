from typing import TYPE_CHECKING
from pprint import pformat

from loguru import logger
from discord_webhook import DiscordWebhook
import requests

from .base import Push

if TYPE_CHECKING:
    from YoutubeStreamNotifyBot.youtube_api_client import LiveBroadcast


class DiscordPush(Push):
    def __init__(self, config: dict):
        self.config = config["discord"]

        self.webhook_url = self.config["webhook url"]
        self.content = self.config["content"]

        self._verify()

    def _verify(self):

        if not self.webhook_url:
            logger.info("Discord webhook url empty, skipping.")
            raise ValueError("Discord webhook url empty, skipping.")

        logger.info("Verification of discord webhook url started.")

        output = requests.get(self.webhook_url).json()

        if not output:
            raise AssertionError(f"Webhook verification failed! Response:\n{pformat(output)}")

        logger.info("Verification of discord webhook url complete.")

    def send(self, channel_object: "LiveBroadcast"):

        dict_ = channel_object.as_dict()

        DiscordWebhook(
            url=self.webhook_url,
            content=self.content.format(**dict_),
            rate_limit_retry=True,
        ).execute()

        logger.info("Notified to discord webhook.")

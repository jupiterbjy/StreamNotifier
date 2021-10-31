from typing import TYPE_CHECKING
from pprint import pformat

from loguru import logger
from discord_webhook import DiscordWebhook
import requests

from .base import Push

if TYPE_CHECKING:
    from TwitchStreamNotifyBot.twitch_api_client import TwitchChannel


class DiscordPush(Push):
    def __init__(self, config: dict):
        self.config = config["discord"]

        self.webhook_url = self.config["webhook_url"]
        self.content = self.config["content"]

        self._verify()

    def _verify(self):

        if not self.webhook_url:
            logger.info("Discord webhook_url empty, skipping.")
            raise ValueError("Discord webhook_url empty, skipping.")

        logger.info("Verification of discord webhook_url started.")

        response = requests.get(self.webhook_url)

        if not response:
            raise AssertionError(f"Webhook verification failed! Response:\n{pformat(response.json())}")

        logger.info("Verification of discord webhook_url complete.")

    def send(self, link, channel_object: "TwitchChannel"):

        dict_ = channel_object.as_dict()
        dict_["link"] = link

        DiscordWebhook(
            url=self.webhook_url,
            content=self.content.format(**dict_),
            rate_limit_retry=True,
        ).execute()

        logger.info("Notified to discord webhook.")

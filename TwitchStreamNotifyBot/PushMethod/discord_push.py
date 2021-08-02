from typing import TYPE_CHECKING
import time

from loguru import logger
from discord_webhook import DiscordWebhook

from .base import Push

if TYPE_CHECKING:
    from TwitchStreamNotifyBot.twitch_api_client import TwitchChannel


class DiscordPush(Push):
    def __init__(self, config: dict):
        self.config = config["discord"]

        self.webhook_url = self.config["webhook url"]
        self.content = self.config["content"]

        self._verify()

    def _verify(self):

        if not self.webhook_url:
            logger.info("Discord webhook url empty, skipping.")
            raise ValueError("Discord webhook URL emtpy")

        delete_delay = 1

        logger.info("Verification of discord webhook url started.")

        # verify url
        webhook = DiscordWebhook(
            url=self.webhook_url,
            content=f"Webhook Verified! WIll be auto deleted in {delete_delay} seconds!",
        )
        sent = webhook.execute()
        time.sleep(delete_delay)
        webhook.delete(sent)

        logger.info("Verification of discord webhook url complete.")

    def send(self, link, channel_object: "TwitchChannel"):

        dict_ = channel_object.as_dict()
        dict_["link"] = link

        DiscordWebhook(
            url=self.webhook_url,
            content=self.content.format(**dict_),
            rate_limit_retry=True,
        ).execute()

        logger.info("Notified to discord webhook.")

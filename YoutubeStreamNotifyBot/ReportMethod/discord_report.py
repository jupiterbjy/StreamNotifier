"""
Reports status to discord
"""
import traceback

import requests
from loguru import logger
from discord_webhook import DiscordWebhook, DiscordEmbed


REPORT_CONFIG = {
    "twitch": {
        "username": "Twitch Notifier",
        "icon": "https://imgur.com/ftY3HKz.png",
        "color": "a364fe"
    }
}


class DiscordReport:
    def __init__(self, url, username, icon, color):
        self.url = url
        self.user_config = {
            "username": username,
            "icon": icon,
            "color": color
        }

        self.report = self._report if self.verify() else lambda *arg: print("Dummy report called")

    def verify(self):
        output = None
        try:
            # verify webhook URL
            assert (output := requests.get(self.url))

        except KeyError:
            # no key exists
            logger.info("Discord Reporting Webhook URL is empty.")

        except AssertionError:
            # invalid webhook_url or unstable network
            try:
                response = output.json()
            except AttributeError:
                response = None

            logger.warning(f"Discord Reporting Webhook URL is invalid. Response: {response}")

        else:
            return True

        return False

    @staticmethod
    def create_embed(**kwargs):
        return DiscordEmbed(**kwargs)

    def _report(self, **kwargs):
        webhook = DiscordWebhook(self.url, **self.user_config, **kwargs)

        result = webhook.execute()

        try:
            result.raise_for_status()
        except Exception:
            traceback.print_exc(limit=4)

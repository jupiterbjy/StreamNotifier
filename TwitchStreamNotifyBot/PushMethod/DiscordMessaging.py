import time
import traceback

from loguru import logger
from discord_webhook import DiscordWebhook


class DiscordPush:

    @staticmethod
    def verify(configuration: dict) -> bool:

        delete_delay = 2

        logger.info("Verification of discord webhook url started.")

        # verify key
        try:
            webhook_url = configuration["push methods"]["discord"]["webhook"]
        except KeyError:
            logger.info("Discord Webhook URL not found.")
            return False

        # verify url
        try:
            webhook = DiscordWebhook(url=webhook_url, content=f"Webhook Verified! Auto deleted in {delete_delay} seconds!")
            sent = webhook.execute()
            time.sleep(delete_delay)
            webhook.delete(sent)

        except Exception:
            traceback.print_exc()

            logger.critical("Webhook verification Failed! Check traceback!")
            return False

        logger.info("Verification of discord webhook url complete.")
        return True

    @staticmethod
    def send_closure(configuration: dict):
        webhook_url: str = configuration["push methods"]["discord"]["webhook"]
        content_form: str = configuration["push methods"]["discord"]["content"]

        def send(content):
            DiscordWebhook(url=webhook_url, content=content_form.format(content), rate_limit_retry=True).execute()
            logger.info("Notified to discord webhook.")

        return send

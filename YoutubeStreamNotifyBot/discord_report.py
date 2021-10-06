"""
Reports status to discord
"""
import traceback
from typing import Union, Dict

import requests
from loguru import logger
from discord_webhook import DiscordWebhook, DiscordEmbed


def report_closure(config: dict):
    output = None
    try:
        # verify webhook URL
        webhook_url = config["discord_report_webhook"]
        assert (output := requests.get(webhook_url))

    except KeyError:
        # no key exists
        logger.info("Discord Reporting Webhook URL is empty")

    except AssertionError:
        # invalid webhook url or unstable network
        try:
            response = output.json()
        except AttributeError:
            response = None

        logger.warning(f"Discord Reporting Webhook URL is invalid. Response: {response}")

    else:
        # return report if complete

        def report(title="StreamNotifier Status", desc="", fields: Union[Dict[str, str], None] = None):
            embed = DiscordEmbed(title=title, color='ff0000', description=desc)
            embed.set_timestamp()

            if fields:
                try:
                    for title, value in fields.items():
                        if value == "":
                            value = None
                        embed.add_embed_field(name=title, value=str(value))

                except Exception:
                    traceback.print_exc(limit=3)

            result = DiscordWebhook(webhook_url, embeds=[embed]).execute()

            try:
                result.raise_for_status()
            except Exception as err:
                traceback.print_exception(err, err, err.__traceback__)

        return report

    # else just pass dummy
    def dummy(*args, **kwargs):
        pass

    return dummy

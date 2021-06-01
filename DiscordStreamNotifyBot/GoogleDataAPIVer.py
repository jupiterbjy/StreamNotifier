#!/usr/bin/python3

import argparse
import pathlib
import json
import trio
from requests.exceptions import ConnectionError, MissingSchema
from loguru import logger

from youtube_api_client import GoogleClient, VideoInfo
from DiscordMessaging import webhook_closure, embed_closure
from RequestExtension import channel_live_check_gen

# End of import --------------


JSON_PATH = pathlib.Path(__file__).parent.absolute().joinpath("configuration.json")


async def check_new_vid():
    pass


async def check_live(client, channel_id, config_dict):

    logger.debug("[{}] task start", channel_id)

    gen_instance = channel_live_check_gen(channel_id, config_dict["interval"])

    notification_callbacks_list = []

    # if webhook is not empty add embedding
    if url := config_dict["push tokens"]["discord webhook"]:
        bot = webhook_closure(url)
        # validate webhook first using empty string
        try:
            bot("")
        except (ConnectionError, MissingSchema) as err:
            logger.critical("Connection/Schema Error! "
                            "Is provided discord webhook url is valid? "
                            "Disabling discord notification!")

            logger.critical("Message: {}", err)

        else:
            discord_config = config_dict["discord webhook"]
            embed_builder = embed_closure(json_data["discord webhook"], config_dict["desc_start"], config_dict["desc_end"])

            def sender(vid_info: VideoInfo):
                bot(content=discord_config["content"], embeds=[embed_builder(vid_info.video_id, vid_info.description)])

            notification_callbacks_list.append(sender)

    # same for telegram
    if config_dict["push tokens"]["telegram bot token"]:
        logger.info("Telegram bot is not supported yet. Ignoring token.")

    # drive loop
    async for _ in gen_instance:
        # fetch lives
        live_ = client.get_live_streams(channel_id)[0]

        for notification_callback in notification_callbacks_list:
            notification_callback(live_[0])


async def main_coroutine(config_dict: dict):
    client = GoogleClient(config_dict["api"]["google api"])

    logger.debug("Discord Webhook OK")

    tasks_param = ((client, channel, config_dict) for channel in config_dict["channels"]["youtube"])

    async with trio.open_nursery() as nursery:

        for param in tasks_param:
            nursery.start_soon(check_live, *param)


if __name__ == "__main__":

    # parsing start =================================

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-p",
        "--path",
        metavar="CONFIG_PATH",
        type=pathlib.Path,
        default=pathlib.Path(__file__).absolute().parent.joinpath("configuration.json"),
        help="Path to configuration json file.",
    )

    args_ = parser.parse_args()

    # parsing end ===================================

    json_data = json.loads(args_.path.read_text())

    logger.info("Target Channels: {}", json_data["channels"])

    trio.run(main_coroutine, json_data)

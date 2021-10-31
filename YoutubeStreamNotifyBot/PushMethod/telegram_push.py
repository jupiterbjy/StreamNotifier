from typing import TYPE_CHECKING
from typing import Union
import traceback

from loguru import logger
import telegram

from .base import Push

if TYPE_CHECKING:
    from YoutubeStreamNotifyBot.youtube_api_client import LiveBroadcast


class TelegramPush(Push):
    def __init__(self, config: dict):
        self.config = config["telegram"]

        self.token = self.config["token"]
        self.chat_ids = self.config["chat_id"]

        self.bot: Union[None, telegram.Bot] = None

        self.auth()

    def auth(self):

        if not self.config["enabled"]:
            raise AssertionError("Telegram Push Disabled, skipping.")

        logger.info("Verification of telegram token started.")

        bot = telegram.Bot(token=self.token)
        updates = bot.get_updates()

        effective_chats = set()

        # populate set
        update: telegram.Update

        for update in updates:
            effective_chats.add(update.effective_chat.id)

        # check diff
        not_found = set(self.chat_ids) - effective_chats

        if not_found:
            for chat_id in not_found:
                logger.warning(
                    "Cannot find group chat_id {}, is bot added to the group? Is group inactive?",
                    chat_id,
                )

        self.bot = bot

        reachable = len(self.chat_ids) - len(not_found)
        logger.info(
            "Verification of telegram token completed. {} of {} chats are visible.",
            reachable,
            len(self.chat_ids),
        )

    def send(self, content, channel_object: "LiveBroadcast"):

        dict_ = channel_object.as_dict()
        text = content.format(**dict_)

        for chat_id in self.chat_ids:
            try:
                message: telegram.Message = self.bot.send_message(
                    chat_id=chat_id, text=text
                )
            except Exception:
                traceback.print_exc()
                logger.warning("Failed to send to group chat_id {}.", chat_id)
            else:
                logger.info("Notified to telegram channel {}.", chat_id)
                try:
                    self.bot.pin_chat_message(message.chat_id, message.message_id)
                except Exception:
                    traceback.print_exc()
                    logger.warning(
                        "Not enough permission to pin message on telegram channel {}.", chat_id
                    )

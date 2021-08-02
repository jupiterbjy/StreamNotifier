from typing import TYPE_CHECKING
from typing import Union
import traceback

from loguru import logger
import telegram

from .base import Push

if TYPE_CHECKING:
    from TwitchStreamNotifyBot.twitch_api_client import TwitchChannel


class TelegramPush(Push):
    def __init__(self, config: dict):
        self.config = config["telegram"]

        self.token = self.config["token"]
        self.chat_ids = self.config["chat id"]
        self.content = self.config["content"]

        self.bot: Union[None, telegram.Bot] = None

        self.auth()

    def auth(self):

        if not all((self.token, self.chat_ids, self.content)):
            logger.info("One or more Telegram parameters empty, skipping.")
            raise ValueError()

        logger.info("Verification of telegram token started.")

        bot = telegram.Bot(token=self.token)
        updates = bot.get_updates()

        for chat_id in self.chat_ids:
            for update in updates:
                update: telegram.Update

                logger.debug("Chat id [{}] / name [{}]", update.effective_chat.id, update.effective_chat.title)

                if update.effective_chat.id == chat_id:
                    logger.info("Found effective chat {}", chat_id)
                    break
            else:
                raise AssertionError(
                    "Cannot find given chat id {}, is bot added to the channel?",
                    self.chat_ids,
                )

        self.bot = bot
        logger.info("Verification of telegram token completed.")

    def send(self, link, channel_object: "TwitchChannel"):

        dict_ = channel_object.as_dict()
        dict_["link"] = link

        text = self.content.format(**dict_)

        for chat_id in self.chat_ids:
            try:
                message: telegram.Message = self.bot.send_message(
                    chat_id=chat_id, text=text
                )
            except Exception:
                traceback.print_exc()

            else:
                try:
                    self.bot.pin_chat_message(message.chat_id, message.message_id)
                except Exception:
                    traceback.print_exc()

        logger.info("Notified to telegram channel {}.", self.chat_ids)

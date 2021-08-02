import traceback
from typing import Union

import telegram
from loguru import logger

from .base import Push


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

    def send(self, content):
        for chat_id in self.chat_ids:
            try:
                self.bot.send_message(
                    chat_id=chat_id, text=self.content.format(content)
                )
            except Exception:
                traceback.print_exc()

        logger.info("Notified to telegram channel {}.", self.chat_ids)

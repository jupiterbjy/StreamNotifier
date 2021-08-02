import traceback

import telegram
from loguru import logger


class TelegramPush:
    @staticmethod
    def verify(configuration: dict) -> bool:

        delete_delay = 2

        logger.info("Verification of telegram token started.")

        token = configuration["push methods"]["telegram"]["token"]
        chat_id = configuration["push methods"]["telegram"]["chat id"]

        # verify url
        try:
            bot = telegram.Bot(token=token)
            updates = bot.get_updates()

            for update in updates:
                update: telegram.Update
                if update.effective_chat.id == chat_id:
                    logger.info("Found effective chat {}", chat_id)
                    break

        except Exception:
            traceback.print_exc()

            logger.critical("Telegram verification Failed! Check traceback!")
            return False

        logger.info("Verification of telegram token completed.")
        return True

    @staticmethod
    def send_closure(configuration: dict):
        token: str = configuration["push methods"]["telegram"]["token"]
        content_form: str = configuration["push methods"]["telegram"]["content"]
        chat_id = configuration["push methods"]["telegram"]["chat id"]

        bot = telegram.Bot(token=token)

        def send(content):
            bot.send_message(chat_id=chat_id, text=content_form.format(content))
            logger.info("Notified to telegram channel {}.", chat_id)

        return send

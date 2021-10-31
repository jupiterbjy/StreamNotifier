from typing import TYPE_CHECKING
from typing import Union

import tweepy
from loguru import logger

from .base import Push

if TYPE_CHECKING:
    from TwitchStreamNotifyBot.twitch_api_client import TwitchChannel


class TwitterPush(Push):
    def __init__(self, config: dict):
        self.config = config["twitter"]

        self.content: str = self.config["content"]

        self.api_key = self.config["api_key"]
        self.api_secret = self.config["api_secret_key"]

        self.token = self.config["access_token"]
        self.token_secret = self.config["access_token secret"]

        self.api: Union[None, tweepy.API] = None

        self.auth()

    def auth(self):

        if not all((self.api_key, self.api_secret, self.token, self.token_secret)):
            logger.info("One or more Twitter parameters empty, skipping.")
            raise ValueError("One or more Twitter parameters empty, skipping.")

        logger.info("Twitch auth started.")

        auth = tweepy.OAuthHandler(self.api_key, self.api_secret)

        auth.set_access_token(self.token, self.token_secret)

        self.api = tweepy.API(auth)

        logger.info("Twitch auth complete.")

    def send(self, link, channel_object: "TwitchChannel"):

        dict_ = channel_object.as_dict()
        dict_["link"] = link

        self.api.update_status(self.content.format(**dict_))

        logger.info("Notified to twitter.")

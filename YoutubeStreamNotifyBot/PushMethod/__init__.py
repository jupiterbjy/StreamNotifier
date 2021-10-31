import traceback

from loguru import logger

from . import discord_push, telegram_push, twitter_push


MODULE_AVAILABLE = []


class TwitchChannel:

    def __init__(self, **kwargs):
        # https://dev.twitch.tv/docs/api/reference#get-channel-information

        self.broadcaster_id: Union[None, str] = None
        self.broadcaster_language: Union[None, str] = None
        self.broadcaster_login: Union[None, str] = None
        self.game_id: Union[None, str] = None
        self.game_name: Union[None, str] = None
        self.id: Union[None, str] = None
        self.is_live: Union[None, bool] = None
        self.tag_ids: Union[None, List[str]] = None
        self.thumbnail_url: Union[None, str] = None
        self.title: Union[None, str] = None
        self.delay: Union[None, int] = None
        self.started_at: Union[None, str, datetime] = None
        self.type: Union[None, str] = None

        self.__dict__.update(kwargs)

        # if self.started_at:
        #     self.created_at = date_parser.parse(self.started_at)

    def __repr__(self):
        string = [f"{k}={v}" for k, v in vars(self).items()]
        return f"TwitchChannel({', '.join(string)})"

    def as_dict(self):
        return vars(self)

    def

class Notifier:
    def __init__(self, config):
        self.methods = available_methods(config)
        self.config = config

    def push_notification(self, platform: str, ):


def available_methods(config: dict):
    """Verifies configuration and return list of available push platforms

    Args:
        config: Full configuration file

    Yields:
        baked push platform instances
    """

    if MODULE_AVAILABLE:
        return MODULE_AVAILABLE

    push_config = config["push_methods"]

    for method in (discord_push.DiscordPush, telegram_push.TelegramPush, twitter_push.TwitterPush):
        try:
            instance = method(push_config)

        except Exception as err:
            logger.warning("Got {} while verifying {}", type(err).__name__, method.__name__)
            traceback.print_exc(limit=4)

        else:
            MODULE_AVAILABLE.append(instance)

    return MODULE_AVAILABLE

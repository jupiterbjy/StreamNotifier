from .youtube import YoutubeStreamCheck
from .twitch import TwitchStreamCheck

stream_list = YoutubeStreamCheck, TwitchStreamCheck

def fetch_stream_platforms(config: dict) -> :


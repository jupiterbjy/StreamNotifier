"""
Unnecessary dummy ABC
"""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from YoutubeStreamNotifyBot.youtube_api_client import LiveBroadcast


# This is unnecessary, but for fun


class Push:
    """ABC for all push methods"""

    def send(self, channel_object: "LiveBroadcast"):
        """Formats text with contents and sends to respective platforms."""
        raise NotImplementedError

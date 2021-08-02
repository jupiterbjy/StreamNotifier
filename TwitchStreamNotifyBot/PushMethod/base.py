"""Unnecessary dummy ABC"""


# This is unnecessary, but for fun
class Push:
    """ABC for all push methods"""

    def send(self, content):
        """Formats text with contents and sends to respective platforms."""
        raise NotImplementedError

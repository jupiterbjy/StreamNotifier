import re
import itertools
from typing import Tuple, AsyncGenerator

import trio
import requests
from loguru import logger


async def video_list_gen(channel_id: str, max_results: int, sleep_second: float) -> Tuple[str]:

    # Compile regex pattern
    pattern = re.compile(r'videoIds"[^"]*"([^"]*)')

    url = f"https://www.youtube.com/channel/{channel_id}"

    # Prepare session
    with requests.session() as session:
        while True:

            # get status
            status = get_channel_status(channel_id, session)

            logger.debug("live check returned status: {}", status)

            # if not live wait and rerun.
            if status != "live":
                await trio.sleep(sleep_second)
                continue

            # else keep on
            get = session.get(url)
            hits = pattern.findall(get.text)

            # Fetch unique keys in appearing order, streams are likely to appear at top.
            vid_ids = tuple(k for (k, v), _ in zip(itertools.groupby(hits), range(max_results)))

            logger.debug("Got code {}, found {} video IDs.", get.status_code, vid_ids)

            yield vid_ids


def get_channel_status(channel_id: str, request_session: requests.Session):

    url = f"https://www.youtube.com/channel/{channel_id}/live"

    data = request_session.get(url).text

    live_common_keyword = "Copyright The Closure Library Authors"
    upcoming_only_keyword = "Offline"

    if live_common_keyword in data:
        if upcoming_only_keyword in data:
            return "upcoming"

        return "live"

    return "none"


async def channel_live_check_gen(channel_id: str, sleep_second: float) -> AsyncGenerator[bool, None, None]:
    """
    Use this to drive other APIs. Yield True when there's live.
    """

    url = f"https://www.youtube.com/channel/{channel_id}/live"

    live_common_keyword = "Copyright The Closure Library Authors"
    upcoming_only_keyword = "Offline"

    def check_status(input_string):

        # check if it has closure copyright - if so, there is player.
        if live_common_keyword in input_string:

            # if it also has offline - it means it has offline stream image, so it's upcoming stream.
            if upcoming_only_keyword in input_string:
                return "upcoming"

            return "live"

        # else it's nothing, probably will be redirected to channel main if javascript ran.
        return "none"

    with requests.session() as session:

        # flag to toggle state
        is_live = False

        while data := session.get(url).text:

            status = check_status(data)

            logger.debug("[{}] live check returned status: {}", channel_id, status)

            # if live flag is True, wait until it's not live - essentially waiting for it to stop.
            if is_live:
                if status != "live":
                    is_live = False

                await trio.sleep(sleep_second)
                continue

            # if not live flagged and status is not live, just wait and continue
            if status != "live":
                await trio.sleep(sleep_second)
                continue

            # otherwise set flag and send signal
            is_live = True
            yield True

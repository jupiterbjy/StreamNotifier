## TwitchStreamNotifyBot

This uses Twitch API to determine stream status and broadcast to supported respective platforms.

Primarily built for [Cyannyan](https://cyannyan.com)'s Twitch stream notifications.

---

## Config

```json
{
  "channel name": "<Twitch_channel_name>",
  "polling api": {
    "twitch app id": "<twitch_app_id_here>",
    "twitch app secret": "<twitch_app_secret_here>"
  },
  "push methods": {
    "discord": {
      "webhook": "<discord_webhook_url>",
      "content": "<@&discord_role_id> Live now! {}\nStarted at: {started_at}\nGame: {game_name}"
    },
    "telegram": {
      "token": "<telegram_bot_token>",
      "chat id": ["<telegram_chat_id_here_as_integer>"],
      "content": "Test Push {link}\nStarted at: {started_at}\nGame: {game_name}"
    },
    "twitter": {
      "api key": "<api key>",
      "api secret key": "<api secret key>",
      "bearer token": "Unused for now",
      "access token": "<access token>",
      "access token secret": "<access token secret>",
      "content": "Bot Twitter push test\n\n{link}\nStarted at: {started_at}\nGame: {game_name}"
    },
    "reddit": {
      "reddit api": "Not_available_yet",
      "content": "add_some_mention_thingy_here {link}"
    }
  }
}

```

---

## Config descriptions

Contents will be formatted with keywords.

Available `content` format keywords are:
```python
'game_name': 'osu!',
'title': 'Road to 5* | Join Multi! | VTuber Cyan',
'live': 'https://www.twitch.tv/cyannyan39'
'started_at': '2021-08-03T02:05:11Z',

'game_id': '21465',
'id': '43109063245',
'is_mature': False,
'language': 'en',
'tag_ids': ['6ea6bca4-4712-4ab9-a906-e3336a9d8039'],
'thumbnail_url': 'https://static-cdn.jtvnw.net/previews-ttv/live_user_cyannyan39-{width}x{height}.jpg',

'type': 'live',
'user_id': '585389049',
'user_login': 'cyannyan39',
'user_name': 'CyanNyan39',
'viewer_count': 19
```

These keywords are formatted by `str.format()`. For example:
```python
message = "Test Push {link}\nStarted at: {started_at}\nGame: {game_name}".format(**dict)
```

Becomes

```python
message = "Test Push https://www.twitch.tv/cyannyan39\nStarted at: 2021-08-03T02:05:11Z\nGame: osu!"
```

---

## Example output

### Discord

  ![image](https://user-images.githubusercontent.com/26041217/127901726-b4a4333f-f900-4e3a-94c6-21b9b919b5cc.png)

---

### Telegram

  ![image](https://user-images.githubusercontent.com/26041217/127901680-96beb0c9-a9ff-4eb1-acf5-682dd8a76113.png)

---

### Twitter

  ![image](https://user-images.githubusercontent.com/26041217/127901434-e4528f97-7326-4bd0-ad7a-27b8c8c8f961.png)

## TwitchStreamNotifyBot

This uses Twitch API to determine stream status and broadcast to supported respective platforms.

Primarily built for Cyannyan's Twitch stream notifications.

## Config

Contents will be formatted with link to channel.

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

## Example output

### Discord

  ![image](https://user-images.githubusercontent.com/26041217/127901726-b4a4333f-f900-4e3a-94c6-21b9b919b5cc.png)

---

### Telegram

  ![image](https://user-images.githubusercontent.com/26041217/127901680-96beb0c9-a9ff-4eb1-acf5-682dd8a76113.png)

---

### Twitter

  ![image](https://user-images.githubusercontent.com/26041217/127901434-e4528f97-7326-4bd0-ad7a-27b8c8c8f961.png)

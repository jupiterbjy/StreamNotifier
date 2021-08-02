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
      "content": "<@&discord_role_id> Live now! {}"
    },
    "telegram": {
      "token": "<telegram_bot_token>",
      "chat id": "<telegram_chat_id_here>",
      "content": "add_some_mention_thingy_here {}"
    },
    "twitter": {
      "api key": "<api key>",
      "api secret key": "<api secret key>",
      "bearer token": "Unused for now",
      "access token": "<access token>",
      "access token secret": "<access token secret>",
      "content": "add_some_mention_thingy_here {}"
    },
    "reddit": {
      "reddit api": "Not_available_yet",
      "content": "add_some_mention_thingy_here {}"
    }
  }
}

```

---

## Example output

### Discord

  ![image](https://user-images.githubusercontent.com/26041217/127803081-f5dd773c-7009-4c63-87ea-acacd68fc924.png)

---

### Telegram

  ![image](https://user-images.githubusercontent.com/26041217/127803145-7ab4a122-654b-4299-bfcd-eeb03107c02c.png)

---

### Twitter

  ![image](https://user-images.githubusercontent.com/26041217/127881548-78a49052-a7d5-4bfe-bc6c-05ab2b10ed48.png)

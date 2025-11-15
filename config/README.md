# Configuration Files

This directory contains the unified bot configuration file that can be updated in real-time without restarting the bot.

## bot_config.json

**Single configuration file** containing all dynamic bot settings including photo IDs and reward channels.

### Structure:

```json
{
  "photos": {
    "prizes": "AgACAgIAA...",
    "referral_link": "AgACAgIAA...",
    "sat_opportunities": "AgACAgIAA..."
  },
  "reward_channels": [
    {
      "name": "Channel display name",
      "chat_id": -1001234567890
    }
  ]
}
```

### Photos Section

Photo IDs used throughout the bot for different features.

**How to get photo IDs:**
1. Send any photo to the bot as an admin
2. The bot will reply with the photo's `file_id` and print it to terminal
3. Copy the `file_id` and paste it into the `photos` section

**Available photo keys:**
- `prizes`: Photo for the prizes/rewards info (🎁 Sovrinlar button)
- `referral_link`: Photo for referral link sharing (🔗Taklif havolasi button)
- `sat_opportunities`: Photo for SAT exam opportunities (👇SAT imtixoni beradigan imkoniyatlar button)

### Reward Channels Section

Defines the channels/groups that users get access to when they reach the required referral count (3+ valid referrals).

**Fields:**
- `name`: Display name for the channel (used in logs and invite link names)
- `chat_id`: Telegram chat ID (negative number for channels/groups)

**How to get chat ID:**
1. Add the bot as admin to the channel/group
2. Forward a message from the channel to @userinfobot
3. Look for the "Origin chat" ID

**Important:**
- The bot must be an admin in all reward channels/groups
- The order of channels determines the order of invite link buttons
- If a channel fails to generate an invite link, it will be skipped (check logs)

## Real-time Updates

Changes to `bot_config.json` take effect immediately without restarting the bot:
- File is checked for modifications on each access
- Reloaded automatically when changes detected
- Console shows "✅ Bot config loaded/reloaded" when file is updated

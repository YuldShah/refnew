# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Telegram referral bot built with aiogram 3.x and PostgreSQL. The bot implements a referral system where users invite friends to join mandatory channels. When users accumulate enough valid referrals (default: 3), they gain access to exclusive educational content for SAT preparation.

## Technology Stack

- **Framework**: aiogram 3.4.1+ (async Telegram bot framework)
- **Database**: PostgreSQL with asyncpg
- **Language**: Python 3.x
- **Data Export**: pandas + openpyxl for Excel exports

## Development Commands

### Running the Bot
```bash
python main.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Database Setup
The bot automatically creates required tables on first run via `Database.create_tables()`. Ensure PostgreSQL is running and credentials are configured in `.env`.

## Environment Configuration

Copy `.env.example` to `.env` and configure:

- `BOT_TOKEN`: Telegram bot token from BotFather
- `ADMIN_IDS`: Comma-separated list of admin Telegram IDs
- `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`: PostgreSQL connection details
- `REQUIRED_REFERRALS`: Number of valid referrals needed to access rewards (default: 3)
- `REWARD_LINK`: Telegram invite link for the reward group/channel

**Note**: `MANDATORY_CHATS_IDS` is deprecated. Mandatory channels are now managed through the admin panel and stored in the database.

## Dynamic Configuration

### `config/bot_config.json`
**Unified configuration file** containing all dynamic bot settings (photo IDs and reward channels). Supports real-time updates without bot restart.

The file is monitored for changes and automatically reloaded when modified. Contains:
- **Photos**: Photo IDs for buttons (prizes, referral links, SAT opportunities)
- **Reward Channels**: Channel/group chat IDs for reward access

**Admin Debug Feature**: Admins can send any photo to the bot to get its file_id printed to terminal and sent back in chat. This makes it easy to update photo IDs in the config.

## Architecture

### Entry Point
- `main.py`: Bot initialization, dispatcher setup, middleware registration, router inclusion

### Database Layer
- `database/models.py`: Single `Database` class containing all database operations
  - Connection pooling via asyncpg
  - Table schema creation
  - User, referral, channel, and reward management
  - Manual access control (grant/deny/normal)
  - Admin user ID 19 is excluded from statistics to prevent skewed metrics

### Middleware
- `middleware/subscription.py`: `SubscriptionMiddleware`
  - Checks user subscription to mandatory channels
  - Handles manual access overrides (granted=bypass, denied=block)
  - Skips checks for admins and `/start` command
  - Supports regular messages, callbacks, and inline queries

### Handlers (Router-based)

**User Handlers** (`handlers/user_handlers.py` + submodules):
- `handlers/user/menu_handlers.py`: Start command, main menu navigation
- `handlers/user/referral_handlers.py`: Referral link sharing, inline query handling
- `handlers/user/stats_handlers.py`: User statistics display and refresh
- `handlers/user/reward_handlers.py`: Reward eligibility checking and access
- `handlers/user/rules_handlers.py`: Rules display
- User router aggregates all sub-routers

**Admin Handlers** (`handlers/admin_handlers.py` + submodules):
- `handlers/admin/admin_menu.py`: Admin panel navigation
- `handlers/admin/admin_stats.py`: Top referrers, user lookup, Excel export
- `handlers/admin/admin_stats_router.py`: Stats routing logic
- `handlers/admin/manage_access.py`: Mandatory channel management, manual access control
- Admin router aggregates all sub-routers

### Services
- `services/referral_service.py`: `ReferralService`
  - Referral link generation
  - Referral stats calculation
  - Pending referral validation via channel membership checks
  - Reward eligibility checking and notifications

- `services/admin_service.py`: `AdminService`
  - Top referrers query
  - User info lookup
  - Excel export with multiple sheets (users, referrals, top referrers)

### UI Components
- `keyboards/user_keyboards.py`: User inline keyboards
- `keyboards/admin_keyboards.py`: Admin inline keyboards
- `text/messages.py`: Multilingual message templates (Uzbek/English)
  - `get_text(key, lang, **kwargs)`: Get formatted message by key and language

### Filters
- `filters/user_filters.py`: Custom filters for admin identification

## Key Workflows

### Referral System Flow
1. User receives unique 8-character referral code on registration
2. Shares referral link: `https://t.me/{bot_username}?start={referral_code}`
3. New user joins via link → referral created with `valid=FALSE`
4. When referred user subscribes to all mandatory channels → referral marked `valid=TRUE`
5. Referrer is notified when referral is validated
6. When referrer reaches `REQUIRED_REFERRALS` valid referrals → eligible for reward

### Subscription Validation
- Middleware intercepts all messages/callbacks/inline queries
- Checks `users.manual_access` (1=granted, -1=denied, 0=normal flow)
- For normal flow: checks `get_chat_member` status for each mandatory channel
- If unsubscribed: shows subscription keyboard with channel buttons + "Check Subscription" button
- On "Check Subscription" click: re-validates and calls `validate_user_referrals()` if subscribed

### Admin Features
- **Mandatory Channels**: Add/remove channels that users must subscribe to
- **Manual Access**: Grant/deny access to specific users, bypassing channel checks
- **Statistics**: View top referrers, search users by ID, export all data to Excel
- Excel export includes 3 sheets: user stats, detailed referrals, top 50 referrers

## Database Schema

**users**:
- `id` (serial, primary key)
- `telegram_id` (bigint, unique)
- `username`, `full_name`
- `referral_code` (8-char unique string)
- `language` (default 'uz')
- `manual_access` (0=normal, 1=granted, -1=denied)
- `joined_at`

**referrals**:
- `id`, `referrer_id` (FK to users), `referred_id` (FK to users)
- `valid` (boolean, default FALSE)

**mandatory_channels**:
- `id`, `chat_id` (bigint, unique), `title`, `link`, `created_at`

**rewards**:
- `id`, `user_id` (FK to users), `reward` (JSONB), `generated_at`

## Important Implementation Notes

### Dependency Injection
The `Database` instance is passed via dispatcher context:
```python
dp['db'] = db  # in main.py
# Then in handlers:
async def handler(message: Message, db):
    user = await db.get_user(message.from_user.id)
```

### Message Formatting
- All messages support HTML parse mode (configured as default)
- Use `get_text(key, lang, **kwargs)` for consistent message retrieval
- Messages are stored in `text/messages.py` with placeholders for `.format()`

### Inline Queries
Special handling in middleware for users not subscribed:
- `handlers/user/referral_handlers.py::handle_inline_query_for_not_subbed()`
- Shows "switch_pm" button to redirect to bot

### Referral Validation
Two triggers for validation:
1. User clicks "Check Subscription" button → validates their own pending referrals
2. `ReferralService.check_and_validate_pending_referrals()` → checks all pending referrals for a user

### Excel Export
Uses in-memory BytesIO to avoid file system clutter. Saves to `users_export_{timestamp}.xlsx` in current directory.

## Common Patterns

### Handler Registration
```python
from aiogram import Router, F

router = Router()

@router.message(F.text == "some_text")
async def handler(message: Message, db):
    pass
```

### FSM (Finite State Machine)
Used for multi-step admin operations (e.g., adding channels). States defined inline in handler files.

### Error Handling
- Subscription check failures trigger admin notifications via `_notify_admin()`
- Bot permission errors (TelegramForbiddenError) are caught and logged
- Missing users return `None` from database queries

## Testing Considerations

When testing locally:
- Use separate PostgreSQL database (configure in `.env`)
- Admin user ID 19 is excluded from stats; avoid using this ID for real users
- Test with multiple Telegram accounts to verify referral flow
- Ensure bot is admin in test channels for membership checks

## Localization

Currently supports Uzbek ('uz') and English ('en'). Default is Uzbek. User language preference is stored but `get_user_language()` always returns 'uz' (hardcoded override in database/models.py:170).

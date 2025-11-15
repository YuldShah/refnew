import asyncpg
from typing import List, Optional, Dict
from datetime import datetime
import os
import secrets
import string
import logging
import json

class Database:
    def __init__(self):
        self.pool = None
        # Configuration from environment variables
        self.required_referrals = int(os.getenv('REQUIRED_REFERRALS', '3'))
        self.reward_link = os.getenv('REWARD_LINK', 'https://t.me/addlist/a55Whe4Fa9ozNDky')
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', 5432),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'password'),
            database=os.getenv('DB_NAME', 'refbot'),
            min_size=1,
            max_size=10        )
        await self.create_tables()
    
    async def create_tables(self):
        async with self.pool.acquire() as conn:            
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE NOT NULL,
                    username VARCHAR(255),
                    full_name VARCHAR(255),
                    referral_code VARCHAR(8) UNIQUE,
                    language VARCHAR(2) DEFAULT 'uz',
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    manual_access INTEGER DEFAULT 0
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS referrals (
                    id SERIAL PRIMARY KEY,
                    referrer_id INTEGER REFERENCES users(id),
                    referred_id INTEGER REFERENCES users(id),
                    valid BOOLEAN DEFAULT FALSE
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS mandatory_channels (
                    id SERIAL PRIMARY KEY,
                    chat_id BIGINT UNIQUE NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    link VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS rewards (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL REFERENCES users(id),
                    reward JSONB NOT NULL,
                    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def generate_referral_code(self) -> str:
        """Generate 8-character random string"""
        characters = string.ascii_letters + string.digits
        return ''.join(secrets.choice(characters) for _ in range(8))

    async def add_user(self, telegram_id: int, username: str, full_name: str) -> tuple[bool, str]:
        async with self.pool.acquire() as conn:
            try:
                # Generate unique referral code
                referral_code = None
                for _ in range(10):  # Try up to 10 times to get unique code
                    code = self.generate_referral_code()
                    exists = await conn.fetchval('SELECT id FROM users WHERE referral_code = $1', code)
                    if not exists:
                        referral_code = code
                        break
                
                if not referral_code:
                    raise Exception("Could not generate unique referral code")
                
                await conn.execute(
                    'INSERT INTO users (telegram_id, username, full_name, referral_code, language) VALUES ($1, $2, $3, $4, $5)',
                    telegram_id, username, full_name, referral_code, 'uz'
                )
                return True, referral_code
            except asyncpg.UniqueViolationError:
                # Get existing referral code and return it as-is without generating a new one.
                existing_code = await conn.fetchval('SELECT referral_code FROM users WHERE telegram_id = $1', telegram_id)
                return False, existing_code
                
    async def get_user(self, telegram_id: int) -> Optional[dict]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow('SELECT * FROM users WHERE telegram_id = $1', telegram_id)
            return dict(row) if row else None
            
    async def get_user_by_referral_code(self, referral_code: str) -> Optional[dict]:
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow('SELECT * FROM users WHERE referral_code = $1', referral_code)
            return dict(row) if row else None
            
    async def add_referral(self, referrer_telegram_id: int, referred_telegram_id: int, referral_code: str) -> bool:
        async with self.pool.acquire() as conn:
            try:
                # Get user IDs from telegram IDs
                referrer_id = await conn.fetchval('SELECT id FROM users WHERE telegram_id = $1', referrer_telegram_id)
                referred_id = await conn.fetchval('SELECT id FROM users WHERE telegram_id = $1', referred_telegram_id)
                
                if not referrer_id:
                    logging.error(f"Referrer ID not found for telegram_id: {referrer_telegram_id}")
                    return False
                    
                if not referred_id:
                    logging.error(f"Referred ID not found for telegram_id: {referred_telegram_id}")
                    return False
                
                # Check if referral already exists
                existing = await conn.fetchval(
                    'SELECT id FROM referrals WHERE referrer_id = $1 AND referred_id = $2',
                    referrer_id, referred_id
                )
                if existing:
                    logging.info(f"Referral already exists: {referrer_id} -> {referred_id}")
                    return True
                
                await conn.execute(
                    'INSERT INTO referrals (referrer_id, referred_id, valid) VALUES ($1, $2, $3)',
                    referrer_id, referred_id, False
                )
                logging.info(f"Added new referral: {referrer_id} -> {referred_id}")
                return True
            except Exception as e:
                logging.error(f"Error adding referral: {str(e)}")
                return False

    async def validate_referral(self, referrer_telegram_id: int, referred_telegram_id: int):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                UPDATE referrals SET valid = TRUE 
                WHERE referrer_id = (SELECT id FROM users WHERE telegram_id = $1) 
                AND referred_id = (SELECT id FROM users WHERE telegram_id = $2)
            ''', referrer_telegram_id, referred_telegram_id)

    async def get_unvalidated_referrals(self, referrer_telegram_id: int) -> List[dict]:
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT r.*, u.telegram_id as referred_telegram_id 
                FROM referrals r 
                JOIN users u ON r.referred_id = u.id 
                WHERE r.referrer_id = (SELECT id FROM users WHERE telegram_id = $1) 
                AND r.valid = FALSE
            ''', referrer_telegram_id)
            return [dict(row) for row in rows]
            
    async def get_valid_referrals_count(self, referrer_telegram_id: int) -> int:
        async with self.pool.acquire() as conn:
            return await conn.fetchval('''
                SELECT COUNT(*) FROM referrals 
                WHERE referrer_id = (SELECT id FROM users WHERE telegram_id = $1) 
                AND valid = TRUE
            ''', referrer_telegram_id)
            
    async def get_user_language(self, telegram_id: int) -> str:
        """Always return Uzbek language for all users"""
        return 'uz'
            
    async def update_user_language(self, telegram_id: int, language: str):
        async with self.pool.acquire() as conn:
            await conn.execute('UPDATE users SET language = $1 WHERE telegram_id = $2', language, telegram_id)
            lang = await conn.fetchval('SELECT language FROM users WHERE telegram_id = $1', telegram_id)
            return lang or 'uz'
            
    async def set_user_language(self, telegram_id: int, language: str):
        """Set user's preferred language"""
        return await self.update_user_language(telegram_id, language)
    
    async def validate_user_referrals(self, telegram_id: int) -> Dict[str, int]:
        """Validate any pending referrals for this user"""
        async with self.pool.acquire() as conn:
            # Get user's internal ID
            user_id = await conn.fetchval('SELECT id FROM users WHERE telegram_id = $1', telegram_id)
            if not user_id:
                return {"validated": 0}

            # Check if this user was referred by someone else and that referral is not validated yet
            pending_referrals = await conn.fetch('''
                SELECT r.id FROM referrals r
                WHERE r.referred_id = $1 AND r.valid = FALSE
            ''', user_id)

            # Validate all pending referrals where this user is the referred one
            validated_count = 0
            for ref in pending_referrals:
                await conn.execute('UPDATE referrals SET valid = TRUE WHERE id = $1', ref['id'])
                validated_count += 1

            return {"validated": validated_count}
    
    async def get_reward_access_count(self) -> int:
        """Get count of users who accessed the reward"""
        async with self.pool.acquire() as conn:
            count = await conn.fetchval('''
                SELECT COUNT(DISTINCT r.user_id) FROM rewards r
            ''')
            return count or 0

    async def save_user_reward(self, telegram_id: int, reward_data: dict):
        """Save user's reward data (invite links) to database"""
        
        async with self.pool.acquire() as conn:
            # Get user's internal ID from telegram_id
            user_id = await conn.fetchval('SELECT id FROM users WHERE telegram_id = $1', telegram_id)
            if not user_id:
                raise ValueError(f"User with telegram_id {telegram_id} not found")

            await conn.execute(
                'INSERT INTO rewards (user_id, reward) VALUES ($1, $2)',
                user_id, json.dumps(reward_data)
            )

    async def get_user_reward(self, telegram_id: int) -> Optional[dict]:
        """Get user's saved reward data from database"""
        
        async with self.pool.acquire() as conn:
            # Get user's internal ID from telegram_id
            user_id = await conn.fetchval('SELECT id FROM users WHERE telegram_id = $1', telegram_id)
            if not user_id:
                return None

            result = await conn.fetchval('SELECT reward FROM rewards WHERE user_id = $1', user_id)
            return json.loads(result) if result else None

    async def has_user_accessed_reward(self, telegram_id: int) -> bool:
        """Check if user has already accessed the reward"""
        async with self.pool.acquire() as conn:
            # Get user's internal ID from telegram_id
            user_id = await conn.fetchval('SELECT id FROM users WHERE telegram_id = $1', telegram_id)
            if not user_id:
                return False

            result = await conn.fetchval('SELECT id FROM rewards WHERE user_id = $1', user_id)
            return result is not None
    
    # Mandatory Channels Management
    async def add_mandatory_channel(self, chat_id: int, title: str, link: str = None) -> bool:
        """Add a mandatory channel"""
        async with self.pool.acquire() as conn:
            try:
                await conn.execute(
                    'INSERT INTO mandatory_channels (chat_id, title, link) VALUES ($1, $2, $3)',
                    chat_id, title, link
                )
                return True
            except asyncpg.UniqueViolationError:
                return False
    
    async def remove_mandatory_channel(self, chat_id: int) -> bool:
        """Remove a mandatory channel"""
        async with self.pool.acquire() as conn:
            result = await conn.execute('DELETE FROM mandatory_channels WHERE chat_id = $1', chat_id)
            return result != "DELETE 0"
    
    async def get_mandatory_channels(self) -> List[dict]:
        """Get all mandatory channels"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('SELECT * FROM mandatory_channels ORDER BY created_at')
            return [dict(row) for row in rows]
    
    async def get_mandatory_channel_ids(self) -> List[int]:
        """Get list of mandatory channel IDs"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('SELECT chat_id FROM mandatory_channels')
            return [row['chat_id'] for row in rows]
    
    async def update_mandatory_channel(self, chat_id: int, title: str = None, link: str = None) -> bool:
        """Update mandatory channel info"""
        async with self.pool.acquire() as conn:
            updates = []
            params = []
            param_count = 1
            
            if title is not None:
                updates.append(f'title = ${param_count}')
                params.append(title)
                param_count += 1
            
            if link is not None:
                updates.append(f'link = ${param_count}')
                params.append(link)
                param_count += 1
                
            if not updates:
                return False
                
            params.append(chat_id)
            query = f'UPDATE mandatory_channels SET {", ".join(updates)} WHERE chat_id = ${param_count}'
            result = await conn.execute(query, *params)
            return result != "UPDATE 0"
    
    # Manual Access Management
    async def set_manual_access(self, telegram_id: int, access_level: int) -> bool:
        """Set manual access level for user (0=normal, 1=granted, -1=denied)"""
        async with self.pool.acquire() as conn:
            result = await conn.execute(
                'UPDATE users SET manual_access = $1 WHERE telegram_id = $2',
                access_level, telegram_id
            )
            return result != "UPDATE 0"
    
    async def create_user_with_manual_access(self, telegram_id: int, access_level: int) -> bool:
        """Create user with manual access level"""
        async with self.pool.acquire() as conn:
            try:
                await conn.execute(
                    'INSERT INTO users (telegram_id, manual_access) VALUES ($1, $2)',
                    telegram_id, access_level
                )
                return True
            except asyncpg.UniqueViolationError:
                # User exists, just update access level
                result = await conn.execute(
                    'UPDATE users SET manual_access = $1 WHERE telegram_id = $2',
                    access_level, telegram_id
                )
                return result != "UPDATE 0"
    
    async def get_user_access_status(self, telegram_id: int) -> int:
        """Get user's manual access status"""
        async with self.pool.acquire() as conn:
            result = await conn.fetchval(
                'SELECT manual_access FROM users WHERE telegram_id = $1',
                telegram_id
            )
            return result or 0
    
    async def check_user_access(self, telegram_id: int) -> bool:
        """Check if user has access (either through channels or manual)"""
        access_level = await self.get_user_access_status(telegram_id)
        
        # If manually granted access, allow
        if access_level == 1:
            return True
        
        # If manually denied access, block
        if access_level == -1:
            return False
        
        # Otherwise check channel subscriptions (normal flow)
        return None  # Let middleware handle channel checking

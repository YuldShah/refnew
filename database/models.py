import asyncpg
from typing import List, Optional
from datetime import datetime
import os
import secrets
import string

class Database:
    def __init__(self):
        self.pool = None
    
    async def connect(self):
        self.pool = await asyncpg.create_pool(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', 5432),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'password'),
            database=os.getenv('DB_NAME', 'refbot'),
            min_size=1,
            max_size=10
        )
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
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
                CREATE TABLE IF NOT EXISTS channels (
                    id SERIAL PRIMARY KEY,
                    channel_id BIGINT UNIQUE,
                    title VARCHAR(255),
                    username VARCHAR(255),
                    mandatory BOOLEAN DEFAULT TRUE
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
                # Get existing referral code
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
                
                if not referrer_id or not referred_id:
                    return False
                
                await conn.execute(
                    'INSERT INTO referrals (referrer_id, referred_id, referral_code) VALUES ($1, $2, $3)',
                    referrer_id, referred_id, referral_code
                )
                return True
            except:
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

    def get_mandatory_channel_ids(self) -> List[int]:
        """Get mandatory channel IDs from environment variables"""
        channel_ids_str = os.getenv('MANDATORY_CHATS_IDS', '')
        if not channel_ids_str:
            return []
        try:
            return [int(channel_id.strip()) for channel_id in channel_ids_str.split(',') if channel_id.strip()]
        except ValueError:
            return []

    async def get_user_language(self, telegram_id: int) -> str:
        async with self.pool.acquire() as conn:
            lang = await conn.fetchval('SELECT language FROM users WHERE telegram_id = $1', telegram_id)
            return lang or 'uz'

    async def update_user_language(self, telegram_id: int, language: str):
        async with self.pool.acquire() as conn:
            await conn.execute('UPDATE users SET language = $1 WHERE telegram_id = $2', language, telegram_id)
            lang = await conn.fetchval('SELECT language FROM users WHERE telegram_id = $1', telegram_id)
            return lang or 'uz'

    async def update_user_language(self, telegram_id: int, language: str):
        async with self.pool.acquire() as conn:
            await conn.execute('UPDATE users SET language = $1 WHERE telegram_id = $2', language, telegram_id)

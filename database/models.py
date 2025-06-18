import asyncpg
from typing import List, Optional, Dict
from datetime import datetime
import os
import secrets
import string
import logging

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
                SELECT id FROM referrals 
                WHERE referred_id = $1 AND valid = FALSE
            ''', user_id)
            
            # Validate all pending referrals where this user is the referred one
            validated_count = 0
            for ref in pending_referrals:
                await conn.execute('UPDATE referrals SET valid = TRUE WHERE id = $1', ref['id'])
                validated_count += 1
                
            return {"validated": validated_count}

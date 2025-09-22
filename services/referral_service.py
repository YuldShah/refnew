from database.models import Database
from typing import Dict, Any, Optional

class ReferralService:
    def __init__(self, db: Database):
        self.db = db
    
    async def get_user_referral_link(self, user_id: int, bot_username: str = None) -> str:
        """Get user's referral link"""
        user = await self.db.get_user(user_id)
        if user and user.get('referral_code'):
            if not bot_username:
                bot_username = "your_bot_username"  # Fallback
            return f"https://t.me/{bot_username}?start={user['referral_code']}"
        return None
    
    async def get_referral_stats(self, user_id: int) -> Dict[str, Any]:
        """Get user's referral statistics (excluding admin user ID 19 from counts)"""
        async with self.db.pool.acquire() as conn:
            if user_id == 19:
                # For admin user, return 0 to not display inflated stats
                return {
                    'total_referrals': 0,
                    'valid_referrals': 0,
                    'pending_referrals': 0
                }
            
            # Get total referrals (excluding referrals to admin user ID 19)
            total_referrals = await conn.fetchval('''
                SELECT COUNT(*) FROM referrals r 
                JOIN users u ON r.referred_id = u.id 
                WHERE r.referrer_id = (SELECT id FROM users WHERE telegram_id = $1)
                AND u.telegram_id != 19
            ''', user_id)
            
            # Get valid referrals (excluding referrals to admin user ID 19)
            valid_referrals = await conn.fetchval('''
                SELECT COUNT(*) FROM referrals r 
                JOIN users u ON r.referred_id = u.id 
                WHERE r.referrer_id = (SELECT id FROM users WHERE telegram_id = $1) 
                AND r.valid = TRUE 
                AND u.telegram_id != 19
            ''', user_id)
            
            # Get pending referrals
            pending_referrals = total_referrals - valid_referrals
            
            return {
                'total_referrals': total_referrals or 0,
                'valid_referrals': valid_referrals or 0,
                'pending_referrals': pending_referrals or 0
            }
    
    async def get_referred_users(self, user_id: int) -> list:
        """Get list of users referred by this user (excluding admin user ID 19)"""
        async with self.db.pool.acquire() as conn:
            if user_id == 19:
                # For admin user, return empty list to not display inflated referrals
                return []
            
            referred_users = await conn.fetch("""
                SELECT u.full_name, u.username, r.valid, u.joined_at
                FROM referrals r 
                JOIN users u ON r.referred_id = u.id 
                WHERE r.referrer_id = (SELECT id FROM users WHERE telegram_id = $1)
                AND u.telegram_id != 19
                ORDER BY u.joined_at DESC
            """, user_id)
            
            return [dict(user) for user in referred_users]
    
    async def check_and_validate_pending_referrals(self, user_id: int, bot) -> Dict[str, Any]:
        """Check subscription status of pending referrals and validate them if subscribed"""
        # Get user ID from telegram ID
        user = await self.db.get_user(user_id)
        if not user:
            return {"validated": 0, "still_pending": 0}
            
        # Get pending referrals (excluding referrals to admin user ID 19)
        async with self.db.pool.acquire() as conn:
            pending_referrals = await conn.fetch("""
                SELECT r.id, r.referrer_id, r.referred_id, u.telegram_id as referred_telegram_id
                FROM referrals r 
                JOIN users u ON r.referred_id = u.id 
                WHERE r.referrer_id = $1 AND r.valid = FALSE AND u.telegram_id != 19
            """, user['id'])
            
            if not pending_referrals:
                return {"validated": 0, "still_pending": 0}
                  # Get channel IDs to check subscriptions
            channel_ids = await self.db.get_mandatory_channel_ids()
            if not channel_ids:
                # If no mandatory channels, validate all pending referrals
                for ref in pending_referrals:
                    await conn.execute("UPDATE referrals SET valid = TRUE WHERE id = $1", ref['id'])
                return {"validated": len(pending_referrals), "still_pending": 0}
            
            # Check each pending referral
            validated_count = 0
            for ref in pending_referrals:
                referred_telegram_id = ref['referred_telegram_id']
                
                # Check if user is subscribed to all channels
                subscribed = True
                for channel_id in channel_ids:
                    try:
                        member = await bot.get_chat_member(channel_id, referred_telegram_id)
                        if member.status not in ['member', 'administrator', 'creator']:
                            subscribed = False
                            break
                    except Exception as e:
                        subscribed = False
                        break
                
                # If subscribed, validate the referral
                if subscribed:
                    await conn.execute("UPDATE referrals SET valid = TRUE WHERE id = $1", ref['id'])
                    validated_count += 1
            
            return {
                "validated": validated_count,
                "still_pending": len(pending_referrals) - validated_count
            }
        
    async def check_and_notify_reward_eligibility(self, user_id: int, bot) -> Dict[str, Any]:
        """Check if user is eligible for reward and send notification"""
        stats = await self.get_referral_stats(user_id)
        valid_count = stats.get('valid_referrals', 0)
        
        # Check if user just reached the reward threshold
        if valid_count >= self.db.required_referrals:
            # Check if user hasn't been notified yet
            if not await self.db.has_user_accessed_reward(user_id):
                # Send reward notification
                await self._send_reward_notification(user_id, bot)
                return {
                    "reward_eligible": True,
                    "just_qualified": True,
                    "valid_referrals": valid_count
                }
            else:
                return {
                    "reward_eligible": True,
                    "just_qualified": False,
                    "valid_referrals": valid_count
                }
        
        return {
            "reward_eligible": False,
            "just_qualified": False,
            "valid_referrals": valid_count,
            "remaining_referrals": self.db.required_referrals - valid_count
        }
    
    async def _send_reward_notification(self, user_id: int, bot):
        """Send reward eligibility notification to user"""
        from text.messages import get_text
        
        try:
            text = get_text('reward_eligible_notification', 'uz', 
                          required_referrals=self.db.required_referrals)
            await bot.send_message(user_id, text)
        except Exception as e:
            # Log error but don't raise - notification failure shouldn't break flow
            import logging
            logging.error(f"Failed to send reward notification to {user_id}: {e}")

from database.models import Database
from typing import Dict, Any, Optional, List
import pandas as pd
import io
import os
from datetime import datetime

class AdminService:
    def __init__(self, db: Database):
        self.db = db
    
    async def get_top_referrers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top N referrers ordered by valid referrals count"""
        async with self.db.pool.acquire() as conn:
            query = """
            SELECT 
                u.telegram_id, 
                u.username, 
                u.full_name, 
                COUNT(r.id) as referral_count
            FROM 
                users u
            JOIN 
                referrals r ON u.id = r.referrer_id
            WHERE 
                r.valid = TRUE
            GROUP BY 
                u.telegram_id, u.username, u.full_name
            ORDER BY 
                referral_count DESC
            LIMIT $1
            """
            rows = await conn.fetch(query, limit)
            return [dict(row) for row in rows]
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Dict[str, Any]:
        """Get detailed user info by telegram_id including referral stats"""
        user = await self.db.get_user(telegram_id)
        if not user:
            return None
            
        # Get referral stats
        async with self.db.pool.acquire() as conn:
            valid_referrals = await conn.fetchval(
                'SELECT COUNT(*) FROM referrals r JOIN users u ON r.referred_id = u.id WHERE r.referrer_id = $1 AND r.valid = TRUE',
                user['id']
            )
            
            pending_referrals = await conn.fetchval(
                'SELECT COUNT(*) FROM referrals r JOIN users u ON r.referred_id = u.id WHERE r.referrer_id = $1 AND r.valid = FALSE',
                user['id']
            )
          # Add stats to user data
        user['valid_referrals'] = valid_referrals
        user['pending_referrals'] = pending_referrals
        
        return user
        
        return user
    
    async def export_users_data(self) -> str:
        """Export all users and referrals to Excel file with referral stats"""
        try:
            # Get all users with their referral statistics
            async with self.db.pool.acquire() as conn:
                # Get users with referral stats
                users_query = '''
                    SELECT 
                        u.id,
                        u.telegram_id,
                        u.username,
                        u.full_name,
                        u.age,
                        u.phone_number,
                        u.education_status,
                        u.sat_goal,
                        u.registration_completed,
                        u.referral_code,
                        u.language,
                        u.joined_at,
                        COALESCE(valid_refs.count, 0) as valid_referrals,
                        COALESCE(pending_refs.count, 0) as pending_referrals,
                        COALESCE(valid_refs.count, 0) + COALESCE(pending_refs.count, 0) as total_referrals
                    FROM 
                        users u
                    LEFT JOIN (
                        SELECT referrer_id, COUNT(*) as count 
                        FROM referrals 
                        WHERE valid = TRUE 
                        GROUP BY referrer_id
                    ) valid_refs ON u.id = valid_refs.referrer_id
                    LEFT JOIN (
                        SELECT referrer_id, COUNT(*) as count 
                        FROM referrals 
                        WHERE valid = FALSE 
                        GROUP BY referrer_id
                    ) pending_refs ON u.id = pending_refs.referrer_id
                    ORDER BY u.joined_at
                '''
                
                users = await conn.fetch(users_query)
                  # Get detailed referrals data
                referrals = await conn.fetch('''
                    SELECT 
                        r.id, 
                        u1.telegram_id as referrer_telegram_id, 
                        u1.username as referrer_username, 
                        u1.full_name as referrer_name,
                        u2.telegram_id as referred_telegram_id, 
                        u2.username as referred_username, 
                        u2.full_name as referred_name,
                        r.valid
                    FROM 
                        referrals r
                    JOIN 
                        users u1 ON r.referrer_id = u1.id
                    JOIN 
                        users u2 ON r.referred_id = u2.id
                    ORDER BY r.id DESC
                ''')
                
                # Get top referrers summary
                top_referrers = await conn.fetch('''
                    SELECT 
                        u.telegram_id,
                        u.username,
                        u.full_name,
                        COUNT(r.id) as total_valid_referrals
                    FROM 
                        users u
                    JOIN 
                        referrals r ON u.id = r.referrer_id
                    WHERE 
                        r.valid = TRUE
                    GROUP BY 
                        u.telegram_id, u.username, u.full_name
                    ORDER BY 
                        total_valid_referrals DESC
                    LIMIT 50
                ''')
            
            # Convert to DataFrames
            users_df = pd.DataFrame([dict(user) for user in users])
            referrals_df = pd.DataFrame([dict(ref) for ref in referrals])
            top_referrers_df = pd.DataFrame([dict(ref) for ref in top_referrers])
            
            # Create Excel file in memory
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Users sheet with referral stats
                users_df.to_excel(writer, sheet_name='Users with Stats', index=False)
                
                # All referrals details
                referrals_df.to_excel(writer, sheet_name='All Referrals', index=False)
                
                # Top referrers summary
                top_referrers_df.to_excel(writer, sheet_name='Top Referrers', index=False)
            
            # Save file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(os.getcwd(), f'users_export_{timestamp}.xlsx')
            
            with open(file_path, 'wb') as f:
                f.write(output.getvalue())
                
            return file_path
        except Exception as e:
            print(f"Export error: {e}")
            return None

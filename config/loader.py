import json
import os
from typing import List, Dict, Optional

# Cache for loaded config
_config_cache = None
_last_modified = None

def _load_config() -> dict:
    """Load bot configuration from JSON file (real-time, checks for file changes)"""
    global _config_cache, _last_modified

    config_path = os.path.join(os.path.dirname(__file__), 'bot_config.json')

    try:
        # Check if file was modified since last load
        current_modified = os.path.getmtime(config_path)

        # Reload if file changed or not loaded yet
        if _config_cache is None or _last_modified != current_modified:
            with open(config_path, 'r', encoding='utf-8') as f:
                _config_cache = json.load(f)
            _last_modified = current_modified
            print(f"✅ Bot config loaded/reloaded from {config_path}")

        return _config_cache
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error loading bot_config.json: {e}")
        # Return default fallback config
        return {
            "photos": {},
            "reward_channels": [
                {"name": "Bepul darslar guruhi", "chat_id": -1003087849002},
                {"name": "Bepul darslar kanali", "chat_id": -1002914914573},
                {"name": "Muhokama guruhi", "chat_id": -1003077395393}
            ]
        }

def get_photo(key: str) -> Optional[str]:
    """Get photo ID by key from config"""
    config = _load_config()
    return config.get('photos', {}).get(key)

def get_reward_channels() -> List[Dict[str, any]]:
    """Get reward channel configurations from config"""
    config = _load_config()
    return config.get('reward_channels', [])

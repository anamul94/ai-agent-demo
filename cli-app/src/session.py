import os
import json
import uuid
from pathlib import Path
from agno.storage.sqlite import SqliteStorage
from .constant import DB_FILE, TABLE_NAME, USER_FILE

def ensure_tmp_dir():
    Path("tmp").mkdir(exist_ok=True)

def get_user_id():
    """Get or create user ID"""
    ensure_tmp_dir()
    
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            data = json.load(f)
            return data.get('user_id')
    return None

def save_user_id(user_id):
    """Save user ID to file"""
    ensure_tmp_dir()
    
    with open(USER_FILE, 'w') as f:
        json.dump({'user_id': user_id}, f)

def create_session_id():
    """Generate random session ID"""
    return str(uuid.uuid4())

def get_storage():
    """Get SQLite storage instance"""
    ensure_tmp_dir()
    return SqliteStorage(table_name="agent_sessions", db_file=DB_FILE)

# def get_user_sessions(user_id):
#     """Get all sessions for a user"""
#     storage = get_storage()
#     # This would need to be implemented based on agno's storage API
#     # For now, return empty list
#     return []
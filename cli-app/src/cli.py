#!/usr/bin/env python3
"""
AI Agent CLI - Beautiful command-line interface for AI agents
"""

import os
import sys
import signal
from dotenv import load_dotenv
from .agent_app import create_agent
from .ui import console, select_model, show_welcome, get_or_create_user, select_session_mode
from .chat import chat_loop
# from session import get_storage
from .dbtest import get_last_session_id_by_user
from .session import create_session_id

load_dotenv(".env")

def signal_handler(sig, frame):
    console.print("\n👋 Goodbye!", style="cyan bold")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    current_dir = os.environ.get('ORIGINAL_PWD', os.getcwd())
    
    try:
        # User setup
        user_id = get_or_create_user()
        
        # Model selection
        model, model_name = select_model()
        
        # Session setup
        try:
            last_session = get_last_session_id_by_user(user_id)
            if last_session:
                console.print(f"Last session ID: {last_session}", style="yellow")
                session_id, is_new = select_session_mode()
            else:
                session_id = create_session_id()
        except Exception:
            console.print("⚠️ Database not initialized, creating new session", style="yellow")
            session_id = create_session_id()
        
        # storage = get_storage()
        
        # Create agent
        agent = create_agent(
            model=model, 
            base_dir=current_dir,
            user_id=user_id,
            session_id=session_id,
        )
        console.print("✅ Agent initialized successfully", style="green")
        
    except Exception as e:
        console.print(f"❌ Failed to initialize agent: {e}", style="red")
        sys.exit(1)
    
    show_welcome(current_dir, model_name)
    chat_loop(agent, current_dir)

if __name__ == "__main__":
    main()
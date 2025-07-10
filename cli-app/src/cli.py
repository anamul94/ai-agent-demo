#!/usr/bin/env python3
"""
AI Agent CLI - Beautiful command-line interface for AI agents
"""

import os
import sys
import signal
from dotenv import load_dotenv
from agent_app import create_agent
from ui import console, select_model, show_welcome
from chat import chat_loop

load_dotenv(".env")

def signal_handler(sig, frame):
    console.print("\n👋 Goodbye!", style="cyan bold")
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    current_dir = os.environ.get('ORIGINAL_PWD', os.getcwd())
    
    try:
        model, model_name = select_model()
        agent = create_agent(model=model, base_dir=current_dir)
        console.print("✅ Agent initialized successfully", style="green")
    except Exception as e:
        console.print(f"❌ Failed to initialize agent: {e}", style="red")
        sys.exit(1)
    
    show_welcome(current_dir, model_name)
    chat_loop(agent, current_dir)

if __name__ == "__main__":
    main()
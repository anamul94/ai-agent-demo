#!/usr/bin/env python3
"""
AI Agent CLI - Beautiful command-line interface for AI agents

A CLI application that provides a beautiful interface for interacting with
AI agents powered by Ollama and the Agno framework.

Features:
- Beautiful Rich-based UI with panels and formatting
- Streaming responses with real-time display
- Shell command execution capabilities
- Current directory context awareness
- Graceful exit handling

Usage:
    python src/cli.py
    
Or if installed system-wide:
    my-cli
"""

import os
import sys
import signal
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from agno.models.ollama import Ollama
from agno.models.aws import Claude, AwsBedrock
from agno.models.groq import Groq
from agent_app import create_agent

from dotenv import load_dotenv
load_dotenv(".env")
console = Console()

def signal_handler(sig, frame):
    console.print("\n👋 Goodbye!", style="cyan bold")
    sys.exit(0)

def main():
    # Setup signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    # Get the current working directory where the command was executed
    # For global installation, use ORIGINAL_PWD if available, otherwise use current directory
    current_dir = os.environ.get('ORIGINAL_PWD', os.getcwd())
    
    # Initialize agent with current directory as base_dir
    try:
        ollama = Ollama(id="qwen3:latest")
        # Use inference profile ARN for Claude 4
        claude = Claude(id="apac.anthropic.claude-sonnet-4-20250514-v1:0")
        agent = create_agent(model=ollama, base_dir=current_dir)
        console.print("✅ Agent initialized successfully", style="green")
    except Exception as e:
        console.print(f"❌ Failed to initialize agent: {e}", style="red")
        sys.exit(1)
    
    # Welcome message
    welcome_text = f"""
# 🤖 AI Agent CLI

**Current Directory:** `{current_dir}`
**Agent Model:** Qwen3 (via Ollama)

Type your message and press Enter to chat with the agent.
Type 'exit', 'quit', or press Ctrl+C to exit.
    """
    
    console.print(Panel(
        Markdown(welcome_text),
        title="Welcome",
        border_style="cyan",
        padding=(1, 2)
    ))
    
    # Main loop
    while True:
        try:
            # Get user input
            user_message = Prompt.ask("[bold cyan]You[/bold cyan]", console=console)
            
            # Check for empty input
            if not user_message.strip():
                continue
                
            # Check for exit commands
            if user_message.lower() in ["exit", "quit", "bye"]:
                console.print("👋 Goodbye!", style="cyan bold")
                break
            
            # Add current directory context (use the directory where command was executed)
            context_message = f"Current working directory: {current_dir}\n\nUser message: {user_message}"
            
            # Show message panel
            console.print(Panel(
                user_message,
                title="💬 Your Message",
                border_style="cyan",
                padding=(1, 2)
            ))
            
            # Get response from agent
            console.print("🤔 Agent thinking...", style="yellow")
            
            try:
                response_content = ""
                for res in agent.run(context_message, stream=True):
                    if hasattr(res, 'content') and res.content:
                        response_content += res.content
                        print(res.content, end="", flush=True)
                
                print()  # New line after streaming
                
                # Show final response in panel
                if response_content.strip():
                    console.print(Panel(
                        Markdown(response_content),
                        title="🤖 Agent Response",
                        border_style="blue",
                        padding=(1, 2)
                    ))
                
            except Exception as agent_error:
                console.print(f"❌ Agent error: {agent_error}", style="red")
            
            console.print()  # Add spacing
            console.print("[dim]Ready for next message...[/dim]")
            
        except KeyboardInterrupt:
            console.print("\n👋 Goodbye!", style="cyan bold")
            break
        except EOFError:
            console.print("\n👋 Goodbye!", style="cyan bold")
            break
        except Exception as e:
            console.print(f"❌ Unexpected error: {e}", style="red")
            console.print("Continuing...", style="yellow")
            # Don't break, continue the loop

if __name__ == "__main__":
    main()
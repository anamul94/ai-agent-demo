import os
from rich.prompt import Prompt
from ui import console, show_message, show_response

def chat_loop(agent, current_dir):
    """Main chat loop"""
    while True:
        try:
            user_message = Prompt.ask("[bold cyan]You[/bold cyan]", console=console)
            
            if not user_message.strip():
                continue
                
            if user_message.lower() in ["exit", "quit", "bye"]:
                console.print("👋 Goodbye!", style="cyan bold")
                break
            
            context_message = f"Current working directory: {current_dir}\n\nUser message: {user_message}"
            
            show_message(user_message)
            console.print("🤔 Agent thinking...", style="yellow")
            
            try:
                response_content = ""
                run_metrics=""
                stream_lines = 0
                
                for res in agent.run(context_message, stream=True):
                    if hasattr(res, 'content') and res.content:
                        response_content += res.content
                        print(res.content, end="", flush=True)
                        stream_lines += res.content.count('\n')
                        
                        if hasattr(res, 'event') and res.event == "RunCompleted":
                            # RunCompleted events may contain final metrics
                            if hasattr(res, 'metrics'):
                                run_metrics = res.metrics
                    
                # Clear streaming output
                print(f"\033[{stream_lines + 1}A\033[J", end="")
                
                # Show formatted response
                # console.print(f"""userid {agent.user_id}.. session: {agent.session_id}""", style="red")
                show_response(response_content, run_metrics)
                
            except Exception as agent_error:
                console.print(f"❌ Agent error: {agent_error}", style="red")
            
            console.print()
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
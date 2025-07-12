from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from src.models import get_available_models, create_model
from src.session import get_user_id, save_user_id, create_session_id, get_storage
from src.dbtest import get_last_session_id_by_user

console = Console()

def select_model():
    """Let user select AI model"""
    models = get_available_models()
    
    model_list = "\n".join([f"{k}. {v['name']}" for k, v in models.items()])
    
    console.print(Panel(
        f"[bold cyan]Select AI Model[/bold cyan]\n\n{model_list}",
        title="Model Selection",
        border_style="green"
    ))
    
    while True:
        choice = Prompt.ask("Choose model (1-3)", choices=list(models.keys()))
        
        try:
            model, model_name = create_model(choice)
            console.print(f"✅ Selected: {model_name}", style="green")
            return model, model_name
            
        except Exception as e:
            console.print(f"❌ Failed to initialize model: {e}", style="red")
            console.print("Please try another model.", style="yellow")

def show_welcome(current_dir, model_name):
    welcome_text = f"""
# 🤖 AI Agent CLI

**Current Directory:** `{current_dir}`
**Agent Model:** {model_name}

Type your message and press Enter to chat with the agent.
Type 'exit', 'quit', or press Ctrl+C to exit.
    """
    
    console.print(Panel(
        Markdown(welcome_text),
        title="Welcome",
        border_style="cyan",
        padding=(1, 2)
    ))

def show_message(message, title="💬 Your Message"):
    console.print(Panel(
        message,
        title=title,
        border_style="cyan",
        padding=(1, 2)
    ))

def show_response(response_content, metrics=None):
    if response_content.strip():
        # Main response
        console.print(Panel(
            Markdown(response_content),
            title="🤖 Agent Response",
            border_style="blue",
            padding=(1, 2)
        ))
        
        # Metrics section
        if metrics:
            import json
            if isinstance(metrics, str):
                try:
                    metrics = json.loads(metrics)
                except:
                    pass
            
            if isinstance(metrics, dict):
                metrics_text = "\n".join([f"**{k}:** {v}" for k, v in metrics.items()])
            else:
                metrics_text = str(metrics)
            
            console.print(Panel(
                Markdown(f"**Metadata:**\n{metrics_text}"),
                title="📊 Metrics",
                border_style="dim",
                padding=(0, 1)
            ))

def get_or_create_user():
    """Get existing user or create new one"""
    user_id = get_user_id()
    
    if not user_id:
        console.print(Panel(
            "[bold yellow]Welcome! Please provide your user information.[/bold yellow]",
            title="User Setup",
            border_style="yellow"
        ))
        
        user_id = Prompt.ask("Enter your username or email")
        save_user_id(user_id)
        console.print(f"✅ User ID saved: {user_id}", style="green")
    else:
        console.print(f"👋 Welcome back, {user_id}!", style="cyan")
    
    return user_id

def select_session_mode():
    """Ask user to create new or continue previous session"""
    
    console.print(Panel(
        "[bold cyan]Session Options[/bold cyan]\n\n"
        "1. Create new session\n"
        "2. Continue previous session",
        title="Session Selection",
        border_style="blue"
    ))
    
    choice = Prompt.ask("Choose option (1-2)", choices=["1", "2"])
    
    if choice == "1":
        session_id = create_session_id()
        console.print(f"✅ New session created: {session_id}...", style="green")
        return session_id, True
    else:
        # For now, create new session (previous session retrieval would need more implementation)
        session_id = get_last_session_id_by_user(get_user_id())
        console.print(f"📝 Starting previous session: {session_id}...", style="yellow")
        return session_id, False
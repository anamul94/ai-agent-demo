from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from models import get_available_models, create_model

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

def show_response(response_content):
    if response_content.strip():
        console.print(Panel(
            Markdown(response_content),
            title="🤖 Agent Response",
            border_style="blue",
            padding=(1, 2)
        ))
# 🤖 AI Agent CLI

A beautiful command-line interface for interacting with AI agents powered by Ollama and Agno framework.

## 🎬 Demo

![AI Agent CLI Demo](https://raw.githubusercontent.com/anamul94/ai-agent-demo/main/cli-app/video/demo.gif)

*AI Agent CLI demonstration showing real-time interactions and features*

## ✨ Features

- 🎨 Beautiful CLI interface with Rich formatting
- 🔄 Streaming responses with real-time display
- 🛠️ Shell command execution capabilities
- 📁 Current directory context awareness
- 🎯 Easy to use and install
- 🚀 System-wide availability

## 📋 Prerequisites

- Python 3.12+
- [UV package manager](https://docs.astral.sh/uv/getting-started/installation/)
- API keys for AI providers (see below)

### Required API Keys

Before running the CLI, you need to set up API keys for the AI providers:

```bash
# For AWS Bedrock (Claude, Nova)
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="your-region"

# For Groq
export GROQ_API_KEY="your-groq-api-key"

#For Openrouter
export OPENROUTER_API_KEY="openrouter key"

# For Ollama (local)
# Install Ollama and pull model
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull qwen3:latest
```

**Add to your ~/.bashrc or ~/.zshrc:**
```bash
echo 'export AWS_ACCESS_KEY_ID="your-access-key"' >> ~/.bashrc
echo 'export AWS_SECRET_ACCESS_KEY="your-secret-key"' >> ~/.bashrc
echo 'export AWS_REGION="your-region"' >> ~/.bashrc
echo 'export GROQ_API_KEY="your-groq-api-key"' >> ~/.bashrc
echo 'export OPENROUTER_API_KEY="openrouter key"'>> ~/.bashrc
source ~/.bashrc
```

## 🚀 Installation

### Option 1: System-wide Installation (Recommended)

1. Clone and navigate to the project directory:
   ```bash
   git clone <repository-url>
   cd cli-app
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run the installation script:
   ```bash
   chmod +x install.sh
   ./install.sh
   ```

4. Add ~/.local/bin to PATH (if not already):
   ```bash
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

5. Now you can run from anywhere:
   ```bash
   my-cli
   ```

### Option 2: Development Mode

1. Navigate to the project directory:
   ```bash
   cd cli-app
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run directly:
   ```bash
   uv run python src/cli.py
   ```

## 🎯 Usage

### Starting the CLI

```bash
# If installed system-wide
my-cli

# Or run directly
uv run python src/cli.py
```

### Using the CLI

1. **Start a conversation**: Type your message and press Enter
2. **View responses**: The agent will respond with beautiful formatting
3. **Execute commands**: Ask the agent to run shell commands
4. **Exit**: Type `exit`, `quit`, `bye`, or press `Ctrl+C`

### Example Interactions

```
You: Hello, what's the current directory?
🤖 Agent Response: [Beautiful formatted response with current directory info]

You: List the files in this directory
🤖 Agent Response: [Agent uses shell tools to list files]

You: What's the weather like?
🤖 Agent Response: [Agent responds with weather information]
```

## 🏗️ Project Structure

```
cli-app/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── cli.py              # Main CLI application
│   ├── agent_app.py        # Agent configuration
│   └── main.py             # Alternative entry point
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── README.md               # This file
├── install.sh              # Installation script
└── main.py                 # Simple entry point
```

## ⚙️ Configuration

### Agent Configuration

The agent is configured in `src/agent_app.py`:

- **Model**: Qwen3 via Ollama
- **Tools**: Shell command execution
- **Features**: Streaming responses, markdown formatting, tool call display

### Customization

You can modify the agent behavior by editing `src/agent_app.py`:

```python
def create_agent(model):
    return Agent(
        model=model,
        tools=[
            ShellTools(),
            # Add more tools here
        ],
        instructions="Your custom instructions here",
        show_tool_calls=True,
        markdown=True,
        stream=True,
    )
```

## 🛠️ Development

### Running in Development Mode

```bash
# Install dependencies
uv sync

# Run the CLI
uv run python src/cli.py

# Or run the alternative main
uv run python src/main.py
```

### Adding New Features

1. **Add new tools**: Import and add tools in `src/agent_app.py`
2. **Modify UI**: Update the CLI interface in `src/cli.py`
3. **Change model**: Update the model configuration in `create_agent()`

## 🐛 Troubleshooting

### Common Issues

1. **"Failed to initialize agent" / API Key Errors**
   - Ensure API keys are set in environment variables
   - Check your ~/.bashrc for correct API key exports
   - Verify AWS credentials: `aws sts get-caller-identity`
   - For Ollama: Ensure service is running: `ollama serve`

2. **"Command not found: my-cli"**
   - Run the install script: `./install.sh`
   - Ensure `~/.local/bin` is in your PATH
   - Check if the script is executable: `ls -la ~/.local/bin/my-cli`

3. **"Module not found" errors**
   - Run `uv sync` to install dependencies
   - Ensure you're in the correct directory

4. **"Table 'agent_sessions' not found"**
   - This is normal on first run - the app will create new sessions
   - Database tables are created automatically

5. **Model-specific issues**
   - **Ollama**: Pull the model: `ollama pull qwen3:latest`
   - **AWS Bedrock**: Check region and model availability
   - **Groq**: Verify API key is valid

### Debug Mode

For debugging, you can run with verbose output:

```bash
# Run with Python's verbose mode
uv run python -v src/cli.py
```

## 📝 License

This project is open source. Feel free to modify and distribute.

## 🤝 Contributing

1. Fork the project
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section
2. Ensure all prerequisites are installed
3. Verify Ollama is running and the model is available
4. Check the project structure matches the documentation

---

**Enjoy chatting with your AI agent! 🚀**
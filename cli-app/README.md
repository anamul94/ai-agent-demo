# 🤖 AI Agent CLI

A beautiful command-line interface for interacting with AI agents powered by Ollama and Agno framework.

## 🎬 Demo

[![AI Agent CLI Demo](https://img.youtube.com/vi/aSQECXkZuzE/0.jpg)](https://youtu.be/aSQECXkZuzE)

*Click to watch the full demo on YouTube - see the AI Agent CLI in action!*

## ✨ Features

- 🎨 Beautiful CLI interface with Rich formatting
- 🔄 Streaming responses with real-time display
- 🛠️ Shell command execution capabilities
- 📁 Current directory context awareness
- 🎯 Easy to use and install
- 🚀 System-wide availability

## 📋 Prerequisites

- Python 3.12+
- [Ollama](https://ollama.ai/) installed and running
- Qwen3 model downloaded in Ollama

### Install Ollama and Model

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the Qwen3 model
ollama pull qwen3:latest

# Verify Ollama is running
ollama list
```

## 🚀 Installation

### Option 1: Development Installation

1. Clone or navigate to the project directory:
   ```bash
   cd /path/to/cli-app
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Run the CLI:
   ```bash
   uv run python src/cli.py
   ```

### Option 2: System-wide Installation

1. Make the CLI available system-wide:
   ```bash
   # Create the system-wide script
   mkdir -p ~/.local/bin
   
   # Create the my-cli script
   cat > ~/.local/bin/my-cli << 'EOF'
#!/bin/bash
cd /home/aa/Desktop/WORK/PERSONAL/AGENTS/AGNO/cli-app
uv run python src/cli.py "$@"
EOF
   
   # Make it executable
   chmod +x ~/.local/bin/my-cli
   
   # Add to PATH if not already (add to ~/.bashrc or ~/.zshrc)
   echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. Now you can run from anywhere:
   ```bash
   my-cli
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

1. **"Agent failed to initialize"**
   - Ensure Ollama is running: `ollama serve`
   - Check if Qwen3 model is available: `ollama list`
   - Pull the model if missing: `ollama pull qwen3:latest`

2. **"Command not found: my-cli"**
   - Ensure `~/.local/bin` is in your PATH
   - Check if the script is executable: `ls -la ~/.local/bin/my-cli`

3. **"Module not found" errors**
   - Run `uv sync` to install dependencies
   - Ensure you're in the correct directory

4. **CLI exits after one message**
   - This should be fixed in the current version
   - If it persists, check for error messages

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
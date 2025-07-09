# 🤖 AI Agent CLI - Complete Documentation

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Troubleshooting](#troubleshooting)
- [Development](#development)
- [API Reference](#api-reference)

## Overview

AI Agent CLI is a powerful command-line interface that provides seamless interaction with AI agents powered by multiple LLM providers including Ollama, AWS Bedrock (Claude), and Groq. Built with the Agno framework, it offers a rich terminal experience with streaming responses, tool execution capabilities, and comprehensive system administration features.

## Features

### Core Features
- 🎨 **Rich Terminal UI** - Beautiful interface with panels, markdown rendering, and syntax highlighting
- 🔄 **Streaming Responses** - Real-time response display with live updates
- 🛠️ **Multi-Tool Support** - Shell commands, file operations, Docker management, Python execution
- 🌐 **Multi-Provider Support** - Ollama, AWS Bedrock Claude, Groq models
- 📁 **Context Awareness** - Automatic current directory context injection
- 🚀 **System-wide Installation** - Global CLI access from anywhere
- 💾 **Session History** - Conversation history with configurable retention
- 🔧 **Extensible Architecture** - Easy to add new tools and providers

### Supported Tools
- **Shell Tools** - Execute system commands with safety checks
- **File Tools** - Read, write, search, and manage files
- **Docker Tools** - Container, image, network, and volume management
- **Python Tools** - Code execution, package management with uv

## Prerequisites

### System Requirements
- **Python**: 3.12+
- **Operating System**: Linux, macOS, Windows (WSL recommended)
- **Memory**: 4GB+ RAM recommended
- **Storage**: 1GB+ free space

### AI Provider Requirements

#### Ollama (Local AI)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull required model
ollama pull qwen3:latest

# Verify installation
ollama list
```

#### AWS Bedrock (Claude)
- AWS Account with Bedrock access
- Claude model access enabled in your region
- Proper IAM permissions for Bedrock

#### Groq (Cloud AI)
- Groq API account
- Valid API key

## Installation

### Option 1: Development Installation

```bash
# Clone/navigate to project
cd /path/to/cli-app

# Install dependencies
uv sync

# Run directly
uv run python src/cli.py
```

### Option 2: System-wide Installation

```bash
# Create system-wide script
mkdir -p ~/.local/bin

# Create launcher script
cat > ~/.local/bin/ai-cli << 'EOF'
#!/bin/bash
cd /home/aa/Desktop/WORK/PERSONAL/AGENTS/AGNO/cli-app
uv run python src/cli.py "$@"
EOF

# Make executable
chmod +x ~/.local/bin/ai-cli

# Add to PATH (if not already)
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Option 3: Docker Installation

```bash
# Build Docker image
docker build -t ai-cli .

# Run container
docker run -it --rm \
  -v $(pwd):/workspace \
  -e AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY \
  ai-cli
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# AWS Bedrock Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-east-1

# Claude Model Configuration (choose one)
CLAUDE_MODEL_ID=apac.anthropic.claude-sonnet-4-20250514-v1:0  # Claude 4 (inference profile)
# CLAUDE_MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0   # Claude 3.5 (direct)

# Groq Configuration
GROQ_API_KEY=your_groq_api_key

# Ollama Configuration (optional)
OLLAMA_HOST=http://localhost:11434
```

### Model Selection

Edit `src/cli.py` to choose your preferred model:

```python
# Option 1: Ollama (Local)
model = Ollama(id="qwen3:latest")

# Option 2: AWS Claude 4 (Inference Profile)
model = Claude(id="apac.anthropic.claude-sonnet-4-20250514-v1:0")

# Option 3: AWS Claude 3.5 (Direct)
model = Claude(id="anthropic.claude-3-5-sonnet-20241022-v2:0")

# Option 4: Groq
model = Groq(id="llama-3.1-70b-versatile")
```

### Agent Customization

Modify `src/agent_app.py` to customize agent behavior:

```python
def create_agent(model, base_dir="/"):
    return Agent(
        model=model,
        tools=[
            ShellTools(base_dir=Path(base_dir)),
            FileTools(base_dir=Path(base_dir)),
            DockerTools(enable_image_management=True),
            PythonTools(base_dir=Path(base_dir), uv_pip_install=True),
        ],
        instructions="Custom agent instructions here",
        show_tool_calls=True,
        markdown=True,
        stream=True,
        num_history_responses=3,
    )
```

## Usage

### Basic Usage

```bash
# Start the CLI
ai-cli

# Example interactions
You: What's the current directory structure?
You: Install numpy using pip
You: Create a Python script to analyze logs
You: Check system memory usage
You: List running Docker containers
```

### Advanced Usage

#### File Operations
```bash
You: Read the contents of config.json
You: Create a backup of all .py files
You: Search for TODO comments in the codebase
You: Generate a project structure diagram
```

#### System Administration
```bash
You: Check system health and performance
You: Monitor disk usage and cleanup old files
You: Analyze system logs for errors
You: Update system packages
```

#### Development Tasks
```bash
You: Set up a Python virtual environment
You: Run unit tests and generate coverage report
You: Deploy the application using Docker
You: Optimize database queries in the project
```

### Command Reference

| Command | Description |
|---------|-------------|
| `exit`, `quit`, `bye` | Exit the CLI |
| `Ctrl+C` | Force exit |
| `help` | Show available commands |
| `clear` | Clear conversation history |

## Architecture

### Project Structure
```
cli-app/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── cli.py              # Main CLI application
│   ├── agent_app.py        # Agent configuration
│   └── main.py             # Alternative entry point
├── tools/
│   └── file.py             # Custom file tools
├── pyproject.toml          # Project configuration
├── uv.lock                 # Dependency lock file
├── .env                    # Environment variables
├── README.md               # Basic documentation
├── DOCUMENTATION.md        # This file
└── Dockerfile              # Container configuration
```

### Core Components

#### CLI Interface (`src/cli.py`)
- Rich-based terminal UI
- Signal handling for graceful exit
- Context injection and message processing
- Streaming response handling

#### Agent Configuration (`src/agent_app.py`)
- Multi-tool agent setup
- Model abstraction layer
- Tool configuration and management
- History and context management

#### Custom Tools (`tools/`)
- Extended file operations
- Project-specific utilities
- Enhanced system integration

### Data Flow

1. **User Input** → CLI captures and validates input
2. **Context Injection** → Current directory and system info added
3. **Agent Processing** → LLM processes request with available tools
4. **Tool Execution** → Agent executes required system operations
5. **Response Streaming** → Real-time response display
6. **History Management** → Conversation context maintained

## Troubleshooting

### Common Issues

#### Agent Initialization Failures

**Issue**: `❌ Failed to initialize agent`

**Solutions**:
```bash
# Check Ollama status
ollama serve
ollama list

# Verify AWS credentials
aws sts get-caller-identity

# Check environment variables
env | grep -E "(AWS|GROQ|OLLAMA)"
```

#### Claude 4 Inference Profile Errors

**Issue**: `Error code: 400 - model ID with on-demand throughput isn't supported`

**Solution**: Use inference profile ID instead of direct model ID:
```python
# ❌ Wrong
claude = Claude(id="anthropic.claude-sonnet-4-20250514-v1:0")

# ✅ Correct
claude = Claude(id="apac.anthropic.claude-sonnet-4-20250514-v1:0")
```

#### Tool Execution Failures

**Issue**: Shell commands fail or hang

**Solutions**:
```bash
# Check base directory permissions
ls -la /path/to/base/dir

# Verify tool configuration
# Edit src/agent_app.py and adjust tool settings
```

#### Memory Issues

**Issue**: High memory usage or crashes

**Solutions**:
- Reduce `num_history_responses` in agent config
- Use lighter models (e.g., Claude Haiku instead of Sonnet)
- Increase system swap space

### Debug Mode

Enable verbose logging:

```bash
# Set debug environment
export AGNO_DEBUG=1
export PYTHONPATH=/path/to/cli-app/src

# Run with verbose output
python -v src/cli.py
```

### Log Analysis

Check application logs:
```bash
# System logs
tail -f /var/log/syslog | grep python

# Application logs (if configured)
tail -f ~/.local/share/ai-cli/logs/app.log
```

## Development

### Setting Up Development Environment

```bash
# Clone repository
git clone <repository-url>
cd cli-app

# Install development dependencies
uv sync --dev

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Code formatting
black src/
isort src/
```

### Adding New Tools

1. Create tool class:
```python
# tools/custom_tool.py
from agno.tools.base import Tool

class CustomTool(Tool):
    def __init__(self):
        super().__init__(name="custom_tool")
    
    def execute(self, **kwargs):
        # Tool implementation
        pass
```

2. Register in agent:
```python
# src/agent_app.py
from tools.custom_tool import CustomTool

def create_agent(model, base_dir="/"):
    return Agent(
        tools=[
            # ... existing tools
            CustomTool(),
        ]
    )
```

### Adding New Model Providers

```python
# src/cli.py
from agno.models.custom import CustomProvider

# In main():
custom_model = CustomProvider(
    api_key=os.getenv("CUSTOM_API_KEY"),
    model_id="custom-model-id"
)
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_cli.py

# Run with coverage
pytest --cov=src tests/

# Integration tests
pytest tests/integration/
```

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Make changes and add tests
4. Run quality checks: `black`, `isort`, `pytest`
5. Commit changes: `git commit -m "Add new feature"`
6. Push branch: `git push origin feature/new-feature`
7. Create Pull Request

## API Reference

### Agent Class

```python
class Agent:
    def __init__(
        self,
        model: Model,
        tools: List[Tool] = None,
        instructions: str = "",
        show_tool_calls: bool = True,
        markdown: bool = True,
        stream: bool = True,
        num_history_responses: int = 3,
    )
    
    def run(self, message: str, stream: bool = None) -> Iterator[Response]
```

### Model Classes

#### Ollama
```python
Ollama(
    id: str,                    # Model ID (e.g., "qwen3:latest")
    host: str = "localhost",    # Ollama host
    port: int = 11434,         # Ollama port
)
```

#### Claude (AWS Bedrock)
```python
Claude(
    id: str,                           # Model/Profile ID
    aws_access_key_id: str = None,     # AWS credentials
    aws_secret_access_key: str = None,
    region: str = "us-east-1",
)
```

#### Groq
```python
Groq(
    id: str,              # Model ID
    api_key: str = None,  # Groq API key
)
```

### Tool Classes

#### ShellTools
```python
ShellTools(
    base_dir: Path = None,     # Working directory
    timeout: int = 30,         # Command timeout
    allowed_commands: List = None,  # Command whitelist
)
```

#### FileTools
```python
FileTools(
    base_dir: Path = None,     # Base directory
    max_file_size: int = 10MB, # Max file size
    allowed_extensions: List = None,  # File type whitelist
)
```

#### DockerTools
```python
DockerTools(
    enable_image_management: bool = True,
    enable_container_management: bool = True,
    enable_network_management: bool = True,
    enable_volume_management: bool = True,
)
```

#### PythonTools
```python
PythonTools(
    base_dir: Path = None,
    uv_pip_install: bool = True,
    list_files: bool = True,
    read_files: bool = True,
    run_code: bool = True,
    run_files: bool = True,
)
```

---

## Support

For issues and questions:
1. Check this documentation
2. Review troubleshooting section
3. Check project issues on GitHub
4. Create new issue with detailed description

## License

This project is open source. See LICENSE file for details.
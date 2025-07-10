#!/bin/bash

# Install script for AI Agent CLI

set -e  # Exit on any error

echo "🚀 Installing AI Agent CLI..."

# Get the current directory
CURRENT_DIR="$(pwd)"

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv is not installed. Please install uv first."
    echo "Visit: https://docs.astral.sh/uv/getting-started/installation/"
    exit 1
fi

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "⚠️ Warning: Ollama is not installed."
    echo "Please install Ollama: curl -fsSL https://ollama.ai/install.sh | sh"
fi

# Create local bin directory if it doesn't exist
mkdir -p ~/.local/bin

# Create the my-cli script
cat > ~/.local/bin/my-cli << EOF
#!/bin/bash
# Store the current working directory where my-cli was called
ORIGINAL_DIR="\$(pwd)"
# Change to the app directory to run the CLI
cd "$CURRENT_DIR"
# Set PYTHONPATH to include src directory and run the CLI
ORIGINAL_PWD="\$ORIGINAL_DIR" PYTHONPATH="$CURRENT_DIR/src:\$PYTHONPATH" uv run python src/cli.py "\$@"
EOF

# Make it executable
chmod +x ~/.local/bin/my-cli

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo "⚠️ ~/.local/bin is not in your PATH."
    echo "Add this line to your ~/.bashrc or ~/.zshrc:"
    echo 'export PATH="$HOME/.local/bin:$PATH"'
    echo ""
    echo "Then run: source ~/.bashrc (or source ~/.zshrc)"
fi

echo "✅ AI Agent CLI installed successfully!"
echo "You can now run 'my-cli' from anywhere in your terminal."
echo ""
echo "Next steps:"
echo "1. Ensure Ollama is running: ollama serve"
echo "2. Pull the Qwen3 model: ollama pull qwen3:latest"
echo "3. Run the CLI: my-cli"
echo ""
echo "For more information, see README.md"
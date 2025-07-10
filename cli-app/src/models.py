from agno.models.ollama import Ollama
from agno.models.aws import Claude, AwsBedrock
from agno.models.groq import Groq

def get_available_models():
    return {
        "1": {"class": Ollama, "id": "qwen3:latest", "name": "Qwen3 (Ollama)"},
        "2": {"class": Claude, "id": "apac.anthropic.claude-sonnet-4-20250514-v1:0", "name": "Claude Sonnet 4"},
        "3": {"class": AwsBedrock, "id": "apac.amazon.nova-pro-v1:0", "name": "Nova Pro"},
    }

def create_model(choice):
    models = get_available_models()
    model_config = models[choice]
    return model_config["class"](id=model_config["id"]), model_config["name"]
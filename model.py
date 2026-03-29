import os
from dotenv import load_dotenv, find_dotenv


class Config:
    def __init__(self):
        # Load environment variables
        load_dotenv(find_dotenv())

        # API Keys
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

        # Validate keys (fail-fast)
        self._validate()

    def _validate(self):
        missing = []

        if not self.google_api_key:
            missing.append("GOOGLE_API_KEY")
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        if not self.anthropic_api_key:
            missing.append("ANTHROPIC_API_KEY")

        if missing:
            raise ValueError(
                f"Missing environment variables: {', '.join(missing)}"
            )


class ModelConfig:
    def __init__(self):
        load_dotenv(find_dotenv())

        # Models (env-driven with fallback defaults)
        self.gemini = os.getenv("MODEL_GEMINI", "gemini-2.5-flash")
        self.gpt = os.getenv("MODEL_GPT", "openai/gpt-4.1")
        self.claude = os.getenv("MODEL_CLAUDE", "claude-sonnet-4-6")

    def as_dict(self):
        return {
            "gemini": self.gemini,
            "gpt": self.gpt,
            "claude": self.claude
        }


class ModelRegistry:
    """
    Centralized model routing layer
    Enables dynamic selection based on use-case
    """

    def __init__(self):
        self.config = ModelConfig()

        self.models = {
            "fast": self.config.gemini,
            "balanced": self.config.gpt,
            "creative": self.config.claude
        }

    def get_model(self, use_case: str = "balanced"):
        return self.models.get(use_case, self.config.gpt)

# create global instances (singleton-like)
config = Config()
model_registry = ModelRegistry()
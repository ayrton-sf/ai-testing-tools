import os
from llm.models import Model


class Config:
    def __init__(self):
        self.openai_api_key = None
        self.anthropic_api_key = None
        model_name = os.getenv("MODEL")
        if not model_name or model_name.strip() == "":
            raise ValueError("MODEL environment variable is not set")
        try:
            self.model = Model(model_name)
        except ValueError:
            raise ValueError(
                f"Invalid model name: {model_name}. Available models: {[m.value for m in Model]}"
            )

        provider = self.model.provider
        self._set_api_key(provider.value)

    def _set_api_key(self, key_name: str):
        api_key = os.getenv(key_name)
        if not api_key:
            raise ValueError(f"{key_name} environment variable is not set")
        setattr(self, key_name.lower(), api_key)


config = Config()

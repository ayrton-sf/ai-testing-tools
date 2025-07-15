from enum import Enum


class Provider(Enum):
    OPENAI = "OPENAI_API_KEY"
    ANTHROPIC = "ANTHROPIC_API_KEY"


class Model(Enum):
    GPT_4_O = (
        "gpt-4o",
        Provider.OPENAI,
    )
    GPT_4_1 = (
        "gpt-4.1",
        Provider.OPENAI,
    )
    O3 = (
        "o3",
        Provider.OPENAI,
    )
    CLAUDE_SONNET_3_5 = (
        "claude-3-5-sonnet-latest",
        Provider.ANTHROPIC,
    )
    CLAUDE_SONNET_3_7 = (
        "claude-3-7-sonnet-latest",
        Provider.ANTHROPIC,
    )
    CLAUDE_SONNET_4 = (
        "claude-sonnet-4-20250514",
        Provider.ANTHROPIC,
    )

    def __new__(cls, value, provider: Provider):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.provider = provider
        return obj

    @property
    def model_name(self) -> str:
        return self.value

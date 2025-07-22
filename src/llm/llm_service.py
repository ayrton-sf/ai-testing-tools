from langchain_core.language_models import BaseLanguageModel
from langchain_core.tools import BaseTool
from langchain_core.prompts import ChatPromptTemplate
from src.tools.claim_check_tool import ClaimCheckTool
from src.tools.claim_extraction_tool import ClaimExtractionTool
from ..tools.criteria_tool import CriteriaEvalTool
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
import pydantic
from typing import Any, Dict, List, Optional, Union
from .models import Model, Provider


class PromptConfig:
    GENERAL_CRITERIA_EVAL = "./prompts/criteria-checking.txt"
    CLAIM_EXTRACTION = "./prompts/claim-extraction.txt"
    CLAIM_CHECK = "./prompts/claim-checking.txt"


class LLMService:
    def __init__(self, api_key: str, model: Optional[Model] = None):
        self.api_key = api_key
        self.model = model

    def _select_language_model(self) -> BaseLanguageModel:
        try:
            llm_factory = {
                Provider.OPENAI: lambda: ChatOpenAI(
                    model=self.model.value,
                    temperature=1,
                    max_retries=3,
                    api_key=pydantic.SecretStr(self.api_key),
                ),
                Provider.ANTHROPIC: lambda: ChatAnthropic(
                    model_name=self.model.value,
                    temperature=0,
                    api_key=pydantic.SecretStr(self.api_key),
                    timeout=None,
                    stop=None,
                    max_retries=3,
                    max_tokens_to_sample=8192,
                ),
            }.get(self.model.provider)

            return llm_factory()

        except Exception as e:
            print(f"Model initialization error: {e}")
            raise

    def _load_prompt(self, prompt_path: str) -> str:
        try:
            with open(prompt_path, "r", encoding="utf-8") as file:
                return file.read().strip()
        except IOError as e:
            print(f"Failed to load prompt from {prompt_path}: {e}")
            raise

    def create_ai_chain(
        self,
        prompt_path: str,
        tools: Optional[List[BaseTool]] = None,
        must_use_tool: Optional[bool] = False,
    ) -> Any:
        try:
            all_tools = tools or []

            llm = self._select_language_model()
            prompt_template = ChatPromptTemplate.from_template(
                self._load_prompt(prompt_path)
            )

            if tools:
                tool_choice = "auto"
                if self.model.provider == Provider.ANTHROPIC:
                    if must_use_tool:
                        tool_choice = "any"
                else:
                    if must_use_tool:
                        tool_choice = "required"
                llm_with_tools = llm.bind_tools(all_tools, tool_choice=tool_choice)
            else:
                llm_with_tools = llm

            def process_response(response):
                tool_map = {tool.name.lower(): tool for tool in all_tools}

                if response.tool_calls:
                    tool_call = response.tool_calls[0]
                    selected_tool = tool_map.get(tool_call["name"].lower())

                    if selected_tool:
                        return selected_tool.invoke(tool_call["args"])

                return response.content

            return prompt_template | llm_with_tools | process_response

        except Exception as e:
            print(f"Chain creation error: {e}")
            raise

    def evaluate_criterion(self, criterion: str, content: str) -> bool:
        prompt = PromptConfig.GENERAL_CRITERIA_EVAL
        return self.create_ai_chain(
            prompt,
            tools=[CriteriaEvalTool()],
            must_use_tool=True,
        ).invoke(
            {
                "criterion": criterion,
                "content": content,
            }
        )

    def extract_claims(self, content: str) -> List[str]:
        prompt = PromptConfig.CLAIM_EXTRACTION
        return self.create_ai_chain(
            prompt,
            tools=[ClaimExtractionTool()],
            must_use_tool=True,
        ).invoke({"content": content})

    def verify_claims(
        self, claims: List[Dict[str, str]], content: str
    ) -> List[Dict[str, Union[str, bool]]]:
        prompt = PromptConfig.CLAIM_CHECK
        return self.create_ai_chain(
            prompt,
            tools=[ClaimCheckTool()],
            must_use_tool=True,
        ).invoke({"claims": claims, "content": content})

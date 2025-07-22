from typing import Dict, List, Optional, Type
from langchain_core.tools import BaseTool
import json_repair
from pydantic import BaseModel

from src.tools.claim_models import ClaimList


class ClaimExtractionTool(BaseTool):
    name: str = "claim_extraction"
    description: str = "Extract claims out of a piece of content."
    args_schema: Type[BaseModel] = ClaimList

    def _run(self, claims: List[str]) -> List[str]:
        try:
            return claims
        except Exception as e:
            print(f"Error creating files: {e}")
            raise

    async def _arun(self, claims: List[str]) -> List[str]:
        return self._run(claims)

    def _parse_input(
        self, tool_input: str | List[str], tool_call_id: Optional[str] = None
    ) -> ClaimList:
        if isinstance(tool_input, str):
            fixed_tool_input = json_repair.loads(tool_input)
        else:
            fixed_tool_input = tool_input

        return fixed_tool_input

from typing import Dict, List, Optional, Type, Union
from langchain_core.tools import BaseTool
import json_repair
from pydantic import BaseModel

from src.tools.claim_models import ClaimCheckList


class ClaimCheckTool(BaseTool):
    name: str = "claim_check"
    description: str = "Check if claims align with the provided content."
    args_schema: Type[BaseModel] = ClaimCheckList

    def _run(self, claim_results: Dict[str, Union[str, bool]]) -> List[str]:
        try:
            return claim_results
        except Exception as e:
            print(f"Error creating files: {e}")
            raise

    async def _arun(self, claim_results: Dict[str, Union[str, bool]]) -> List[str]:
        return self._run(claim_results)

    def _parse_input(
        self, tool_input: str | Dict, tool_call_id: Optional[str] = None
    ) -> ClaimCheckList:
        if isinstance(tool_input, str):
            fixed_tool_input = json_repair.loads(tool_input)
        else:
            fixed_tool_input = tool_input

        return fixed_tool_input

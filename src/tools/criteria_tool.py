from typing import Any, Dict, Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel
from .criteria_tool_input import CriteriaToolInput


class CriteriaEvalTool(BaseTool):
    name: str = "criteria_evaluation"
    description: str = "Evaluate content based on criteria."
    args_schema: Type[BaseModel] = CriteriaToolInput

    def _run(self, result: bool) -> bool:
        try:
            return result
        except Exception as e:
            print(f"Error creating files: {e}")
            raise

    async def _arun(self, result: bool) -> bool:
        return self._run(result)

    def _parse_input(
        self, result: str | bool, tool_call_id: Optional[str] = None
    ) -> Dict[str, Any]:
        if isinstance(result, str):
            fixed_tool_input = bool(result)
        else:
            fixed_tool_input = result

        return fixed_tool_input

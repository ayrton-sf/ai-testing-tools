from typing import Any, Dict, Optional, Type
from langchain_core.tools import BaseTool
from pydantic import BaseModel
import json_repair
from tools.criteria_tool_input import CriteriaToolInput


class CriteriaEvalTool(BaseTool):
    name: str = "criteria_evaluation"
    description: str = "Evaluate content based on criteria."
    args_schema: Type[BaseModel] = CriteriaToolInput

    def _run(self, tool_input: CriteriaToolInput) -> bool:
        try:
            return tool_input.result
        except Exception as e:
            print(f"Error creating files: {e}")
            raise

    async def _arun(self, result: CriteriaToolInput) -> bool:
        return self._run(result)

    def _parse_input(
        self, tool_input: str | Dict, tool_call_id: Optional[str] = None
    ) -> Dict[str, Any]:
        if isinstance(tool_input, str):
            fixed_tool_input = json_repair.loads(tool_input)
        else:
            fixed_tool_input = tool_input

        return fixed_tool_input

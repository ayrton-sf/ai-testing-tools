from typing import Dict, List, Union
from src.claim_checking.claim_checker import ClaimChecker
from src.llm.llm_service import LLMService
from src.data_sources import get_postgres_mcp


class SQLChecker(ClaimChecker):
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def fetch_reference(self, claims: List[str], db_string: str) -> List[str]:
        reference = []
        for claim in claims:
            relevant_content = await self.llm_service.run_mcp_sql_agent(
                input=claim, server=get_postgres_mcp(db_string)
            )
            if relevant_content:
                reference.append(relevant_content)

        return reference

    def chunk_content(self, content: List[Dict]) -> List[Dict]:
        return content

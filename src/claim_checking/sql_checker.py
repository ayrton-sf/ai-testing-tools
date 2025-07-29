from typing import Dict, List, Union
from src.claim_checking.claim_checker import ClaimChecker
from src.llm.llm_service import LLMService
from src.data_sources import get_postgres_mcp


class SQLChecker(ClaimChecker):
    def __init__(self, llm_service: LLMService):
        self.llm_service = llm_service

    async def fetch_reference(self, content: str, db_string: str) -> List[str]:
        query_result = await self.llm_service.run_mcp_sql_agent(
            input=content, server=get_postgres_mcp(db_string)
        )
        return query_result

    def check_claims(
        self, claims: List[Dict[str, str]], content_chunks: List[str]
    ) -> List[Dict[str, Union[str, bool]]]:
        all_claims = [{"claim": claim, "validity": False} for claim in claims]

        for chunk in content_chunks:
            pending = [claim for claim in all_claims if not claim["validity"]]
            if not pending:
                break

            updated = self.llm_service.verify_claims(pending, chunk)

            for claim in updated:
                for existing_claim in all_claims:
                    if existing_claim["claim"] == claim["claim"]:
                        existing_claim["validity"] = claim["validity"]
                        break

        return all_claims

    def chunk_content(self, content: List[str]) -> List[str]:
        pass

from abc import ABC, abstractmethod
from typing import Dict, List, Union


class ClaimChecker(ABC):
    @abstractmethod
    def fetch_reference(self, content: str, **kwargs) -> List[str]:
        """Fetch reference data based on provided arguments."""
        pass

    @abstractmethod
    def chunk_content(self, content: str) -> List[str]:
        """Chunk the content into manageable pieces for claim checking."""
        pass
    
    def check_claims(
        self, claims: List[Dict[str, str]], content_chunks: List
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
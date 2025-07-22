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

    @abstractmethod
    def check_claims(
        self, claims: List[Dict[str, str]], content_chunks: List[str]
    ) -> List[Dict[str, Union[str, bool]]]:
        """Check the claims against the content chunks and return results."""
        pass

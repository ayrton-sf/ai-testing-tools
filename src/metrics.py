from typing import Dict, List, Optional, Union
from .llm.llm_service import LLMService
from src.claim_checking.web_checker import WebChecker
from src.data_sources import DataSource
from src.llm.models import Model


class Metrics:
    def __init__(self, model: str, api_key: str):
        if not model or not model.strip():
            raise ValueError("`model` must be a non‐empty string")
        if not api_key or not api_key.strip():
            raise ValueError("`api_key` must be a non‐empty string")

        try:
            self.model = Model(model)
        except ValueError:
            raise ValueError(f"Invalid model: {model}")

        self.api_key = api_key.strip()
        self.llm_service = LLMService(api_key=self.api_key, model=self.model)

    def criteria_eval(
        self, content: str, criteria: List[str]
    ) -> Dict[str, Union[List[Dict[str, str]], int]]:
        results = []

        for criterion in criteria:
            llm_judgement_result = self.llm_service.evaluate_criterion(
                criterion, content
            )
            results.append(llm_judgement_result)

        total_score = (
            len([result for result in results if result]) / len(criteria) * 100
        )
        return {
            "score": total_score,
            "results": [
                {"criterion": criteria[i], "result": results[i]}
                for i in range(len(criteria))
            ],
        }

    def claim_check(
        self, content: Optional[str], data_source: DataSource, urls: Optional[List[str]]
    ) -> List[Dict[str, Union[str, bool]]]:
        claims = self.llm_service.extract_claims(content)

        checker_factory = {DataSource.WEB: lambda: WebChecker(self.llm_service)}

        checker = checker_factory[data_source]()

        call_args = {}

        if data_source == DataSource.WEB and urls is not None:
            call_args["urls"] = urls

        reference = checker.fetch_reference(**call_args)

        chunked_reference = checker.chunk_content(reference)

        return checker.check_claims(claims=claims, content_chunks=chunked_reference)

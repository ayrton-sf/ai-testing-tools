from typing import Dict, List, Optional, Union
from src.claim_checking.sql_checker import SQLChecker
from .llm.llm_service import LLMService
from src.claim_checking.web_checker import WebChecker
from src.data_sources import DataSource
from src.llm.models import Model


class Metrics:
    def __init__(self, model: str, api_key: str, **kwargs):
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

    async def claim_check(
        self,
        content: Optional[str],
        data_source: DataSource,
        db_string: Optional[str] = None,
        urls: Optional[List[str]] = None,
        query_url: Optional[str] = None,
    ) -> List[Dict[str, Union[str, bool]]]:
        claims = self.llm_service.extract_claims(content)

        for arg_name in data_source.required_args:
            value = locals().get(arg_name)
            if not value or isinstance(value, str) and not value.strip():
                raise ValueError(
                    f"`{arg_name}` is required when data_source is {data_source.name}."
                )

        checker_factory = {
            DataSource.WEB: lambda: WebChecker(self.llm_service),
            DataSource.SQL: lambda: SQLChecker(self.llm_service),
        }

        checker = checker_factory[data_source]()

        call_args = {}

        if data_source == DataSource.SQL:
            call_args["claims"] = claims

        required_args = data_source.required_args

        for arg in required_args:
            call_args[arg] = locals().get(arg)

        reference = await checker.fetch_reference(**call_args)

        chunked_reference = checker.chunk_content(reference)

        claim_check_result = checker.check_claims(claims=claims, content_chunks=chunked_reference)

        score = 0

        for claim in claim_check_result:
            if claim["validity"]:
                score += 1

        score = (score / len(claim_check_result)) * 100

        return {
            "score": score,
            "claims": claim_check_result,
        }

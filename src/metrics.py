from typing import Dict, List, Union
from llm.llm_service import LLMService


class Metrics:
    def __init__(self):
        self.llm_service = LLMService()

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

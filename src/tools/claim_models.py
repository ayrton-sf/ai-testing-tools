from typing import List
from pydantic import BaseModel, Field, RootModel


class ClaimCheckResult(BaseModel):
    claim: str = Field(
        description="A claim extracted from the content.",
        examples=[
            "There are three main branches of research.",
            "The building dates back to the 18th century.",
            "The product is eco-friendly.",
        ],
    )
    validity: bool = Field(
        description="Indicates whether the claim is valid or not.",
        examples=[True, False],
    )


class ClaimList(BaseModel):
    claims: List[str] = Field(
        description="A list of claims extracted from the content",
        examples=[
            [
                "There are three main branches of research in this field.",
                "The building dates back to the 18th century.",
                "The product is eco-friendly.",
            ]
        ],
    )


class ClaimCheckList(BaseModel):
    claim_results: List[ClaimCheckResult] = Field(
        description="A list of claims (with expected validity) to check against the content. Make sure to enclose string in double quotes.",
        examples=[
            [
                {
                    "claim": "There are three main branches of research in this field.",
                    "validity": False,
                },
                {
                    "claim": "The building dates back to the 18th century.",
                    "validity": True,
                },
                {
                    "claim": "The product is eco-friendly.",
                    "validity": False,
                },
            ]
        ],
    )

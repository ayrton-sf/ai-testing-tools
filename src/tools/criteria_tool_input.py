from pydantic import BaseModel, Field


class CriteriaToolInput(BaseModel):
    result: bool = Field(
        description="The result of the evaluation. True if the content meets the criteria, otherwise False.",
    )

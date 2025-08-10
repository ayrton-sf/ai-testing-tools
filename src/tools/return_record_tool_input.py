from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Union

class ReturnRecordToolInput(BaseModel):
    result: Optional[Union[List[Dict],str]] = Field(
        default=None,
        description="Relevant records from the database query. List of records if found, otherwise None. The List must not be wrapped by double quotes."
    )

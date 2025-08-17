from pydantic import BaseModel, Field, RootModel
from typing import Optional, Dict, Any, Union, List

class Metadata(BaseModel):
    Summary: str = Field(default_factory=list, description="A brief summary of the document")
    Title: str
    Author: str
    DateCreated: str
    LastModifiedDate: str
    Publisher: str
    Language: str
    PageCount: Union[int, str]
    SentimentTone: str

class ChangeFormat(BaseModel):
    page: int
    changes: str
    
class SummaryResponse(RootModel[list[ChangeFormat]]):
    pass
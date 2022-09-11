from typing import List, Optional
from pydantic import BaseModel


class MetaData(BaseModel):
    count: int
    q: str
    type: str
    maxResults: int = 100


class Results(BaseModel):
    num: int
    jcn: str
    edinet_code: str
    sec_code: Optional[str] = None
    name_jp: str
    name_eng: str


class GetCompanyResponse(BaseModel):
    metadata: MetaData
    results: List[Results]

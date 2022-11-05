import datetime
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


class FetchCompanyResult(BaseModel):
    num: int
    id: int
    jcn: str
    edinet_code: str
    sec_code: Optional[str] = None
    name_jp: str
    name_eng: str


class GetCompanyResponse_V0(BaseModel):
    metadata: MetaData
    results: List[FetchCompanyResult]


class GetCompanyResponse(BaseModel):
    metadata: MetaData
    results: List[Results]


class DocumentResult(BaseModel):
    id: int
    document_uid: str
    current_fiscalyear_startdate: datetime.date
    current_fiscalyear_enddate: datetime.date
    current_period_enddate: datetime.date
    is_consolidated: bool
    document_type: str
    company_id: int
    accounting_standard_id: int
    dei_industry_code_id: int
    period_type_id: int


class DocumentResponse(BaseModel):
    results: List[DocumentResult]


class FetchFindataResult(BaseModel):
    id: int
    document_id: int
    account_label_id: int
    context_id: int
    dimension_id: int
    ammount: int
    is_consolidated: bool
    qname: str
    name_jp: str


class FetchFindataResponse(BaseModel):
    results: List[FetchFindataResult]
from enum import Enum


class CompanySelectType(Enum):
    jcn = "jcn"
    edinet_code = "edinet_code"
    sec_code = "sec_code"
    name_jp = "name_jp"
    name_eng = "name_eng"

from enum import Enum, IntEnum


class CompanySelectType(Enum):
    jcn = "jcn"
    edinet_code = "edinet_code"
    sec_code = "sec_code"
    name_jp = "name_jp"
    name_eng = "name_eng"


class FinDataDimensionType(IntEnum):
    貸借対照表 = 1
    損益計算書 = 2
    包括利益計算書 = 3
    キャッシュフロー計算書 = 4

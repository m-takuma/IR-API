from fastapi.testclient import TestClient
from controller.main import app
client = TestClient(app)


# 全てのパラメータが適切である場合のテストケース
def test_select_company_allok():
    response = client.get("/company?q=ＫＤＤＩ&type=name_jp&maxResults=200")
    assert response.status_code == 200
    assert response.json() == {
        "metadata": {
            "count": 1,
            "q": "ＫＤＤＩ",
            "type": "name_jp",
            "maxResults": 200
        },
        "results": [
            {
                "num": 1,
                "jcn": "9011101031552",
                "edinet_code": "E04425",
                "sec_code": "9433",
                "name_jp": "ＫＤＤＩ",
                "name_eng": "KDDI CORPORATION"
            }
        ]
    }


# パラメータがない場合のテストケース
def test_select_company_noneprops():
    response = client.get("/company")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": [
                    "query",
                    "q"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            },
            {
                "loc": [
                    "query",
                    "type"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }


# maxResultsが範囲外の場合のテストケース
def test_select_company_butmaxResults():
    response = client.get("/company?q=ＫＤＤＩ&type=name_jp&maxResults=501")
    assert response.status_code == 400
    assert response.json() == {
        "status": 400,
        "message": "パラメーターエラーです"
    }

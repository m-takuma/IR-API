from typing import Union
import psycopg2
import psycopg2.extras
from model.ResponseModel import DocumentResponse, GetCompanyResponse
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import model.Error as Error
import os
from model.PropsModel import CompanySelectType as CompanySelectType
app = FastAPI()

connecter = psycopg2.connect(
    'postgresql://{user}:{password}@{host}:{port}/{dbname}'
    .format(
        user="developer",
        password=os.environ['postgresql_dev_pass'],
        host="postgresql",
        port="5432",
        dbname="api_dev"
    )
)


@app.get("/company", response_model=GetCompanyResponse)
def select_company(
        q: str,
        type: CompanySelectType,
        maxResults: Union[int, None] = 100
        ):
    if (maxResults) <= 0 or int(maxResults) > 500:
        raise Error.ParamException
    result = []
    match type.value:
        case CompanySelectType.jcn.value | CompanySelectType.edinet_code.value:
            result = companeis_find(connecter, f'{q}', type.value, maxResults)
        case (
                CompanySelectType.sec_code.value |
                CompanySelectType.name_jp.value |
                CompanySelectType.name_eng.value
                ):
            result = companeis_find(
                connecter,
                f'%{q}%', type.value, maxResults
                )
        case _:
            raise Error.ParamException
    return JSONResponse(status_code=200, content={
        "metadata": {
            "count": len(result),
            "q": q,
            "type": type.value,
            "maxResults": maxResults
        },
        "results":
            result
    })


'''
@app.post("/company")
async def insert_company(
        jcn: str,
        edinet_code: str,
        name_jp: str,
        name_eng: str,
        sec_code: Union[str, None] = None
        ):
    return ""
'''


@app.get("/document", response_model=DocumentResponse)
def select_document(company_id: int, quarter: bool):
    result = find_documents(connecter, company_id, quarter)
    return JSONResponse(status_code=200, content={
        "results": jsonable_encoder(result)
    })


def companeis_find(connecter, q, type, maxResults):
    with connecter.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            sql_q = "SELECT ROW_NUMBER() OVER(ORDER BY :type ASC) num, \
                jcn, edinet_code, sec_code, name_jp, name_eng \
                FROM companies WHERE :type LIKE ':q' LIMIT :maxResults;"\
                    .replace(':type', '%(type)s')\
                    .replace(':q', '%(q)s')\
                    .replace(':maxResults', '%(maxResults)s')
            cursor.execute(
                sql_q % {
                    'type': type,
                    'q': q,
                    'maxResults': maxResults
                    }
                )
            results = cursor.fetchall()
            dict_result = []
            for row in results:
                dict_result.append(dict(row))
            return dict_result
        except Exception:
            raise Error.ParamException


def company_insert(connecter, jcn, edinet_code, name_jp, name_eng, sec_code):
    pass


def find_documents(connecter, company_id, quarter):
    with connecter.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            if quarter:
                sql_q = "SELECT * FROM fin_documents \
                    WHERE company_id = :company_id \
                        ORDER BY current_period_enddate ASC ;"\
                        .replace(':company_id', '%(company_id)s')
            else:
                sql_q = "SELECT * FROM fin_documents \
                        WHERE company_id = :company_id AND \
                        period_type_id = 1 \
                        ORDER BY current_period_enddate ASC ;"\
                        .replace(':company_id', '%(company_id)s')
            cursor.execute(
                sql_q % {
                    'company_id': company_id,
                }
            )
            results = cursor.fetchall()
            dict_result = []
            for row in results:
                dict_result.append(dict(row))
            return dict_result
        except Exception:
            raise Error.ParamException


@app.exception_handler(Error.ParamException)
async def maxResultsError_handler(request, err: Error.ParamException):
    return JSONResponse(
        status_code=400,
        content={
            "status": err.status_code,
            "message": f"{err.message}"
            }
        )


@app.exception_handler(404)
async def error404_handler(req, err):
    return JSONResponse(
        status_code=err.status_code,
        content={
            "status": err.status_code,
            "message": err.detail
            }
        )

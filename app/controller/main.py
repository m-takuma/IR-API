from typing import Union
import psycopg2
import psycopg2.extras
import os
from model.ResponseModel import DocumentResponse, FetchFindataResponse, GetCompanyResponse, GetCompanyResponse_V0  # NOQA: E501
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
import model.Error as Error
from model.PropsModel import CompanySelectType as CompanySelectType, FinDataDimensionType  # NOQA: E501
from .dbManeger import companeis_find, company_find, fin_data_find, find_documents  # NOQA: E501
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


@app.get("/api/v0/company", response_model=GetCompanyResponse_V0)
def fetch_company(
        q: str,
        type: CompanySelectType,
        maxResults: Union[int, None] = 100
        ):
    if (maxResults) <= 0 or int(maxResults) > 500:
        raise Error.ParamException
    result = []
    match type.value:
        case CompanySelectType.jcn.value | CompanySelectType.edinet_code.value:
            result = company_find(connecter, f'{q}', type.value, maxResults)
        case (
                CompanySelectType.sec_code.value |
                CompanySelectType.name_jp.value |
                CompanySelectType.name_eng.value
                ):
            result = company_find(
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


@app.get("/api/v0/document", response_model=DocumentResponse)
def fetch_document(company_id: int, quarter: bool):
    result = find_documents(connecter, company_id, quarter)
    return JSONResponse(status_code=200, content={
        "results": jsonable_encoder(result)
    })


@app.get("/api/v0/fin_data", response_model=FetchFindataResponse)
def fetch_fin_data(
        document_id: int,
        dimension: Union[FinDataDimensionType, None] = None):
    dimension = dimension.value if dimension is not None else None
    result = fin_data_find(connecter, document_id, dimension)
    return JSONResponse(status_code=200, content={
        "results": jsonable_encoder(result)
    })


@app.get("/api/v0/app_versions")
def get_app_versions():
    def jsonfile():
        with open("./res_files/app_versions.json", mode="rb") as jsonfile:
            yield from jsonfile
    return StreamingResponse(jsonfile(), media_type="application/json")


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

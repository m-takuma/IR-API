import psycopg2.extras
import model.Error as Error


def company_find(connecter, q, type, maxResults):
    with connecter.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            sql_q = "SELECT ROW_NUMBER() OVER(ORDER BY :type ASC) num, * \
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


def fin_data_find(connecter, document_id, dimension):
    with connecter.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
        try:
            if dimension is None:
                sql_q = "SELECT * FROM fin_data \
                        JOIN account_labels label \
                            ON fin_data.account_label_id = label.id \
                        WHERE document_id = :document_id;"\
                            .replace(':document_id', '%(document_id)s')
                cursor.execute(
                    sql_q % {
                        'document_id': document_id
                    })
            else:
                sql_q = "SELECT * FROM fin_data \
                        JOIN account_labels label \
                            ON fin_data.account_label_id = label.id \
                        WHERE document_id = :document_id AND dimension_id = :dimension;"\
                            .replace(':document_id', '%(document_id)s')\
                            .replace(':dimension', '%(dimension)s')
                cursor.execute(
                    sql_q % {
                        'document_id': document_id,
                        'dimension': dimension
                    })
            results = cursor.fetchall()
            dict_result = []
            for row in results:
                print(row)
                dict_result.append(dict(row))
            return dict_result
        except Exception:
            raise Error.ParamException

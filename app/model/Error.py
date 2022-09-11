class ApiException(Exception):
    def __init__(self, status_code, message) -> None:
        super().__init__()
        self.status_code = status_code
        self.message = message


class ParamException(ApiException):
    def __init__(self, status_code=400, message='パラメーターエラーです') -> None:
        super().__init__(status_code, message)

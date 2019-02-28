#encoding=utf-8

from sdk_lib.consts import *

class ExceptionHandler():
    @staticmethod
    def server_exception(e):
        errorType = e.get_error_type()
        requestId = str(e).split("RequestID:")[1].strip()
        httpCode = e.get_http_status()
        errorCode = e.get_error_code()
        errorMessage = e.get_error_msg()
        print (errorType, requestId, httpCode, errorCode, errorMessage)
        if errorCode != None and errorCode in SERVICE_ERROR_CODE:
            return False
        else:
            return True

    @staticmethod
    def client_exception(e):
        errorType = e.get_error_type()
        errorCode = e.get_error_code()
        errorMessage = e.get_error_msg()
        print (errorType, errorCode, errorMessage)
        if errorCode != None and errorCode in CLIENT_ERROR_CODE:
            return False
        else:
            return True


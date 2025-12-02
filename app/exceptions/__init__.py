from http import HTTPStatus

class AppException(Exception):
    '''Base class exception'''
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.message: str = message
        self.status_code: int = status_code

    def to_dict(self) -> dict:
        return {
            "error":{
                "type": self.__class__.__name__,
                "message": self.message,
                "status": self.status_code
            }
        }

class InvalidMagTypeException(AppException):
    '''Class Exception for invalid mag type'''
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.BAD_REQUEST)

class FeatureNotFoundException(AppException):
    '''Class Exception for feature not found'''
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.NOT_FOUND)

class DataNotProvidedException(AppException):
    '''Class Exception for not data input provided'''
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.BAD_REQUEST)

class IDNotProvidedException(AppException):
    '''Class Exception for not provided External or Base ID'''
    def __init__(self, message: str):
        super().__init__(message, HTTPStatus.UNPROCESSABLE_ENTITY)

class UnprocessableSchema(AppException):
    '''Class exception for unprocessable schemas'''
    def __init__(self, message):
        super().__init__(message, HTTPStatus.UNPROCESSABLE_ENTITY)
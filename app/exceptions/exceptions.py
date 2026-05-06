from fastapi import HTTPException, status


class BaseCustomException(HTTPException):
    """Base custom class exception for defined user errors"""

    def __init__(self, detail: str, status_code: int):
        super().__init__(status_code=status_code, detail=detail)
        self.detail: str = detail
        self.status_code: int = status_code


class FeatureNotFoundException(BaseCustomException):
    """Class Exception for feature not found"""

    def __init__(self, code: str):
        self.detail: str = f"Feature of code: {code} was not found."
        super().__init__(detail=self.detail, status_code=status.HTTP_404_NOT_FOUND)


class ExcededFeaturesException(HTTPException):
    """Class Exception for exceding allowed limit of retrieving features"""

    def __init__(self, number_of_features: int):
        self.detail: str = (
            f"The limit for number of features is exceded: {number_of_features}"
        )
        super().__init__(
            detail=self.detail, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )


class InvalidMagTypeException(HTTPException):
    def __init__(self, mag_type: str) -> None:
        self.detail: str = f"Cannot filter by mag type: {mag_type}"
        super().__init__(
            detail=self.detail, status_code=status.HTTP_422_UNPROCESSABLE_CONTENT
        )

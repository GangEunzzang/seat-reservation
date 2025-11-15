from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    code: str
    message: str
    data: T

    @staticmethod
    def success(data: T, message: str = "success", code: str = "200") -> dict:
        return {"code": code, "message": message, "data": data}

    @staticmethod
    def error(message: str, code: str = "ERROR") -> dict:
        return {"code": code, "message": message}

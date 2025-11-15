from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse:
	class Success(BaseModel, Generic[T]):
		code: str
		message: str
		data: T

	class Error(BaseModel):
		code: str
		message: str

	@staticmethod
	def success(data: T, message: str = "success", code: str = "200") -> Success[T]:
		return ApiResponse.Success(code=code, message=message, data=data)

	@staticmethod
	def error(message: str, code: str = "ERROR") -> Error:
		return ApiResponse.Error(code=code, message=message)

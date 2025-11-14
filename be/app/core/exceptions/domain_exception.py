from typing import Any

from app.core.exceptions.error_code import ErrorCode


class DomainException(Exception):
	"""도메인 레이어에서 발생하는 비즈니스 예외"""

	def __init__(self, error_code: ErrorCode, **params: Any):
		self.error_code = error_code
		self.params = params
		self.message = error_code.message_template.format(**params) if params else error_code.message_template
		super().__init__(self.message)

	@property
	def status_code(self) -> int:
		return self.error_code.status_code

	@property
	def code(self) -> int:
		return self.error_code.code

	def to_dict(self) -> dict:
		return {
			"code": self.code,
			"message": self.message
		}

from enum import Enum, unique


@unique
class ReservationStatus(Enum):
	RESERVED = ("reserve", "예약")
	CANCELLED = ("cancel", "취소")

	def __init__(self, code: str, description: str):
		self.code = code
		self.description = description

	@classmethod
	def from_code(cls, code: str) -> "ReservationStatus":
		for status in cls:
			if status.code == code:
				return status
		raise ValueError(f"Invalid ReservationStatus code: {code}")


from dataclasses import dataclass

from app.user.application.ports.inbound.commands import RegisterUserCommand


@dataclass
class User:
	id: int
	user_code: str
	name: str
	department: str
	position: str
	phone_number: str
	episode_id: int

	@classmethod
	def create(cls, register_request: RegisterUserCommand) -> "User":
		return cls(
			id=1,
			user_code=register_request.user_code,
			name=register_request.name,
			department=register_request.department,
			position=register_request.position,
			phone_number=register_request.phone_number,
			episode_id=register_request.episode_id,
		)

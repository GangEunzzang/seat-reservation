from dataclasses import dataclass


@dataclass
class UserRegisterRequest:
	user_code: str
	name: str
	department: str
	position: str
	phone_number: str
	episode_id: int

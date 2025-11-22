from dataclasses import dataclass


@dataclass
class UserRegisterRequest:
	name: str
	department: str
	position: str
	phone_number: str
	episode_id: int

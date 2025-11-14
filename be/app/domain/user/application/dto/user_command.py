from dataclasses import dataclass
from app.domain.user.domain.user_register_request import UserRegisterRequest


@dataclass
class RegisterUserCommand:
    """사용자 등록 커맨드"""
    user_code: str
    name: str
    department: str
    position: str
    phone_number: str
    episode_id: int

    def to_register_request(self):
        return UserRegisterRequest(
            user_code=self.user_code,
            name=self.name,
            department=self.department,
            position=self.position,
            phone_number=self.phone_number,
            episode_id=self.episode_id
        )

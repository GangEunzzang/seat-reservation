from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    user_code: str
    name: str
    department: str | None = None
    position: str | None = None
    phone_number: str | None = None
    episode_id: int

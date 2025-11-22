from pydantic import BaseModel


class UserRegisterRequest(BaseModel):
    name: str
    department: str
    position: str
    phone_number: str
    episode_id: int

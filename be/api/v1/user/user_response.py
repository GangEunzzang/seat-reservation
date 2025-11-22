from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    id: int
    name: str
    department: str
    position: str
    phone_number: str
    episode_id: int

    model_config = ConfigDict(from_attributes=True)

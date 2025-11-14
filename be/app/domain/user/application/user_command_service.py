from app.domain.user.application.dto.user_command import RegisterUserCommand
from app.domain.user.application.ports.inbound.user_command_use_case import UserCommandUseCase
from app.domain.user.application.ports.outbound.user_repository import UserRepository
from app.domain.user.domain.user import User


class UserCommandService(UserCommandUseCase):

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, command: RegisterUserCommand) -> User:
        if await self.user_repository.exists_by_user_code(command.user_code):
            raise ValueError(f"User code '{command.user_code}' already exists")

        user = User.create(command.to_register_request())

        return await self.user_repository.save(user)

    async def delete(self, user_id: int) -> None:
        user = await self.user_repository.find_by_id(user_id)

        if not user:
            raise ValueError(f"User with id {user_id} not found")

        await self.user_repository.delete(user_id)

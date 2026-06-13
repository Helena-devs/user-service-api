from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserListResponse, UserResponse, UserUpdate
from app.services.user_service import UserService


class UserController:
    def __init__(self, db: Session):
        self.service = UserService(db)

    def create_user(self, data: UserCreate) -> UserResponse:
        user = self.service.create_user(data)
        return UserResponse.model_validate(user)

    def get_user(self, user_id: int) -> UserResponse:
        user = self.service.get_user(user_id)
        return UserResponse.model_validate(user)

    def list_users(self, skip: int = 0, limit: int = 100) -> UserListResponse:
        users, total = self.service.list_users(skip=skip, limit=limit)
        return UserListResponse(
            items=[UserResponse.model_validate(user) for user in users],
            total=total,
            skip=skip,
            limit=limit,
        )

    def update_user(self, user_id: int, data: UserUpdate) -> UserResponse:
        user = self.service.update_user(user_id, data)
        return UserResponse.model_validate(user)

    def delete_user(self, user_id: int) -> None:
        self.service.delete_user(user_id)

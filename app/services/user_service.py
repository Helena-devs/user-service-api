from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(self, data: UserCreate) -> User:
        if self.repository.get_by_email(data.email):
            raise ConflictError("User with this email already exists")

        return self.repository.create(
            email=data.email,
            full_name=data.full_name,
            hashed_password=hash_password(data.password),
        )

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    def list_users(self, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        return self.repository.list_users(skip=skip, limit=limit)

    def update_user(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_user(user_id)

        if data.email and data.email != user.email:
            if self.repository.get_by_email(data.email):
                raise ConflictError("User with this email already exists")

        update_fields: dict = {}
        if data.email is not None:
            update_fields["email"] = data.email
        if data.full_name is not None:
            update_fields["full_name"] = data.full_name
        if data.is_active is not None:
            update_fields["is_active"] = data.is_active
        if data.password is not None:
            update_fields["hashed_password"] = hash_password(data.password)

        return self.repository.update(user, **update_fields)

    def delete_user(self, user_id: int) -> None:
        user = self.get_user(user_id)
        self.repository.delete(user)

from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def list_users(self, skip: int = 0, limit: int = 100) -> tuple[list[User], int]:
        query = self.db.query(User)
        total = query.count()
        users = query.order_by(User.id).offset(skip).limit(limit).all()
        return users, total

    def create(self, email: str, full_name: str, hashed_password: str) -> User:
        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, **fields) -> User:
        for key, value in fields.items():
            if value is not None:
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()

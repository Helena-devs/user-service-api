from fastapi import Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository

security = HTTPBearer(
    scheme_name="JWT",
    bearerFormat="JWT",
    description="Paste the access_token from POST /api/v1/auth/login",
    auto_error=False,
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Security(security),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedError("Not authenticated")

    user_id = decode_access_token(credentials.credentials)
    if user_id is None:
        raise UnauthorizedError("Invalid or expired token")

    user = UserRepository(db).get_by_id(int(user_id))
    if not user:
        raise UnauthorizedError("User not found")

    if not user.is_active:
        raise ForbiddenError("User account is inactive")

    return user

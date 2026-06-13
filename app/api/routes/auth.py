from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.controllers.auth_controller import AuthController
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    return AuthController(db)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    controller: AuthController = Depends(get_auth_controller),
) -> UserResponse:
    return controller.register(data)


@router.post("/login", response_model=TokenResponse)
def login(
    data: LoginRequest,
    controller: AuthController = Depends(get_auth_controller),
) -> TokenResponse:
    return controller.login(data)


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)

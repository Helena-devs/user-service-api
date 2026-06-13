from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.controllers.user_controller import UserController
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserListResponse, UserResponse, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    return UserController(db)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    controller: UserController = Depends(get_user_controller),
    _: User = Depends(get_current_user),
) -> UserResponse:
    return controller.create_user(data)


@router.get("", response_model=UserListResponse)
def list_users(
    skip: int = 0,
    limit: int = 100,
    controller: UserController = Depends(get_user_controller),
    _: User = Depends(get_current_user),
) -> UserListResponse:
    return controller.list_users(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    controller: UserController = Depends(get_user_controller),
    _: User = Depends(get_current_user),
) -> UserResponse:
    return controller.get_user(user_id)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    controller: UserController = Depends(get_user_controller),
    _: User = Depends(get_current_user),
) -> UserResponse:
    return controller.update_user(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    controller: UserController = Depends(get_user_controller),
    _: User = Depends(get_current_user),
) -> None:
    controller.delete_user(user_id)

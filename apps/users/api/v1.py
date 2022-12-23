import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from apps.users.crud import user_action
from apps.users.models import User
from apps.users.schemas import CreateUserSchema, UpdateUserSchema
from db.dependencies import get_db

user_router = APIRouter(prefix="/users", tags=["Users"])

logger = logging.getLogger(__name__)


@user_router.get("/")
def get_users(
        limit: int = Query(10),
        offset: int = Query(0),

        db: Session = Depends(get_db)
):
    logger.info(f"Users fetch")
    users = user_action.get_multi(db=db)
    logger.info(f"Users fetched successfully.")
    return users


@user_router.post("/")
def create_user(payload: CreateUserSchema, db: Session = Depends(get_db)):
    logger.info(f"Create new user for '{payload.email}'")
    User.exist_email(db=db, email=payload.email)
    new_user = user_action.create(db=db, obj_in=payload.dict())
    logger.info(f"User '{payload.email}' created successfully.")
    return new_user


@user_router.get("/{id}")
async def get_user(id: str, db: Session = Depends(get_db)):
    user = user_action.get(db=db, id=id)
    return user


@user_router.put("/{id}")
async def update_user(id: str, payload: UpdateUserSchema, db: Session = Depends(get_db)):
    logger.info(f"Update user for '{id}'")
    user_instance = db.query(User).filter(User.id == id).first()
    user = user_action.update(db=db, db_obj=user_instance, obj_in=payload)
    logger.info(f"User '{id}' updated successfully.")
    return user


@user_router.delete("/{id}")
async def delete_user(id: str, db: Session = Depends(get_db)):
    logger.info(f"Delete user for '{id}'")
    user_action.remove(db=db, id=id)
    logger.info(f"User '{id}' deleted successfully.")
    return "Delete successfully"

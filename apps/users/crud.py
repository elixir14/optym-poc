from apps.users.models import User
from apps.users.schemas import CreateUserSchema, UpdateUserSchema
from db.crud import CRUDBase


class CRUDUser(CRUDBase[User, CreateUserSchema, UpdateUserSchema]):
    ...


user_action = CRUDUser(User)

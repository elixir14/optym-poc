from apps.loads.models import Loads
from apps.loads.schemas import CreateLoadsSchema
from db.crud import CRUDBase


class CRUDLoad(CRUDBase[Loads, CreateLoadsSchema, CreateLoadsSchema]):
    ...


load_action = CRUDLoad(Loads)

import logging
from typing import List

from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.orm import Session

from apps.loads.crud import load_action
from apps.loads.schemas import CreateLoadsSchema, LoadsSchema
from db.dependencies import get_db
from optym_poc.core.config import settings
from optym_poc.core.services.azure.azure import azure_scheme
from optym_poc.core.services.azure.message_bus import AzureMessageBus

load_router = APIRouter(prefix="/loads", tags=["Loads"])

logger = logging.getLogger(__name__)


@load_router.get("/", dependencies=[Security(azure_scheme)], response_model=List[LoadsSchema])
def get_loads(
        limit: int = Query(10),
        offset: int = Query(0),
        db: Session = Depends(get_db)
):
    logger.info(f"Loads fetch")
    loads = load_action.get_multi(db=db, skip=offset, limit=limit)
    logger.info(f"Loads fetched successfully.")
    return loads


@load_router.post("/", dependencies=[Security(azure_scheme)], response_model=LoadsSchema)
def create_load(payload: CreateLoadsSchema, db: Session = Depends(get_db)):
    logger.info(f"Create new loads")
    new_load = load_action.create(db=db, obj_in=payload.dict())
    logger.info(f"Loads '{new_load.load_data_id}' created successfully.")
    return new_load


@load_router.get("/{id}", dependencies=[Security(azure_scheme)], response_model=LoadsSchema)
async def get_load(id: str, db: Session = Depends(get_db)):
    logger.info(f"Loads {id} fetch")
    load = load_action.get(db=db, id=id)
    logger.info(f"Loads {id} fetched successfully.")
    return load


@load_router.put("/{id}", dependencies=[Security(azure_scheme)], response_model=LoadsSchema)
async def update_load(id: str, payload: CreateLoadsSchema, db: Session = Depends(get_db)):
    logger.info(f"Update load '{id}'")
    load_instance = load_action.get(db=db, id=id)
    load = load_action.update(db=db, db_obj=load_instance, obj_in=payload)
    logger.info(f"Load '{id}' updated successfully.")
    return load


@load_router.delete("/{id}", dependencies=[Security(azure_scheme)])
async def delete_load(id: str, db: Session = Depends(get_db)):
    logger.info(f"Delete load '{id}'")
    load_action.remove(db=db, id=id)
    logger.info(f"Load '{id}' deleted successfully.")
    return "Delete successfully"


@load_router.post("/send-message")
async def send_message(payload: dict):
    azure_message = AzureMessageBus(
        connection_str=settings.MESSAGEBUS_CONNECTION_STRING,
        queue_name=settings.MESSAGEBUS_QUEUE_NAME
    )
    azure_message.send_single_message(event_data=payload)

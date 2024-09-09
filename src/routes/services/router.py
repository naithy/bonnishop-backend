from bson import ObjectId
from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from .database import collection_name
from .models import list_serial, individual_serial
from src.routes.auth.router import get_current_user
from .schemas import ServiceSchema, ServiceCollection

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("/")
async def get_services():
    data = ServiceCollection(list_serial(collection_name.find()))
    formated_data = [item.model_dump(by_alias=True, include={"id", "name", "image"}) for item in data]
    return formated_data


@router.post("/")
async def create_service(service: ServiceSchema, user: Annotated[dict, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    if collection_name.find_one({"name": service.name}, {"_id": 0}):
        raise HTTPException(status_code=409, detail="Already exists")

    _id = collection_name.insert_one(service.model_dump(by_alias=True))

    return str(_id.inserted_id)


@router.get("/{service_id}")
async def get_service(service_id: str):
    if collection_name.find_one({"_id": ObjectId(service_id)}):
        data = ServiceSchema.model_validate(collection_name.find_one({"_id": ObjectId(service_id)}, {"_id": 0}))
        return data.model_dump(by_alias=True)
    else:
        raise HTTPException(status_code=404, detail="Not Found")


@router.put("/{service_id}")
async def update_service(service_id: str, service: ServiceSchema, user: Annotated[dict, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    if collection_name.find_one({"_id": ObjectId(service_id)}, {"_id": 0}):
        collection_name.replace_one({"_id": ObjectId(service_id)}, service.model_dump(by_alias=True))
    else:
        raise HTTPException(status_code=404, detail="Not Found")


@router.delete("/{service_id}")
async def delete_service(service_id: str, user: Annotated[dict, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    if collection_name.find_one({"_id": ObjectId(service_id)}, {"_id": 0}):
        collection_name.delete_one({"_id": ObjectId(service_id)})

    else:
        raise HTTPException(status_code=404, detail="Not Found")

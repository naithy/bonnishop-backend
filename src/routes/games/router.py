from http import HTTPStatus
from typing import Annotated, Optional
from pydantic import BaseModel, TypeAdapter, Field, Extra
from fastapi import APIRouter, Query, HTTPException, Depends

from .models import list_serial
from .schemas import GameSchema
from src.utils.igdb.main import *
from .database import collection_name
from src.routes.auth.router import get_current_user

router = APIRouter(prefix="/games", tags=["Games"])


class Cover(BaseModel):
    id: Optional[int] = None
    image_id: Optional[str] = None


class Game(BaseModel, extra=Extra.allow):
    id: int
    name: str
    cover: Optional[Cover] = None
    image_id: Optional[str] = Field(default=None, alias="imageId")


@router.get('/')
async def get_games(
        search: Annotated[str | None, Query(description="Search games via IGDB API")] = None,
        where: Annotated[int | None, Query(description="Get game info by ID")] = None,
):
    if search:
        ta = TypeAdapter(list[Game])
        data = ta.validate_python(await get_igdb_games(search))
        for item in data:
            if hasattr(item.cover, "image_id"):
                item.image_id = item.cover.image_id

        return [item.model_dump(by_alias=True, exclude={"cover"}, exclude_none=True) for item in data]

    if where:
        data = Game.model_validate((await igdb_game_info(where))[0])
        data.image_id = data.cover.image_id

        return data.model_dump(by_alias=True, exclude={"cover"})

    if len(list(collection_name.find())) == 0:
        raise HTTPException(status_code=404)

    ta = TypeAdapter(list[GameSchema])
    data = ta.validate_python(list_serial(collection_name.find()))

    return data


@router.get('/{game_id}')
async def get_game(game_id: int):
    if collection_name.find_one({"id": game_id}, {"_id": 0}):
        data = GameSchema.model_validate(collection_name.find_one({"id": game_id}, {"_id": 0}))
        return data.model_dump(by_alias=True)
    else:
        raise HTTPException(status_code=404, detail="Not Found")


@router.post('/', status_code=201)
async def create_game(game: GameSchema, user: Annotated[dict, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    if collection_name.find_one({"id": game.id}, {"_id": 0}):
        raise HTTPException(status_code=409, detail="Already exists")
    collection_name.insert_one(game.model_dump(by_alias=True))


@router.put('/{game_id}', status_code=204)
async def update_game(game_id: int, game: GameSchema, user: Annotated[dict, Depends(get_current_user)]):
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    if collection_name.find_one({"id": game_id}, {"_id": 0}):
        collection_name.replace_one({"id": game_id}, game.model_dump(by_alias=True))
    else:
        raise HTTPException(status_code=404, detail="Not Found")


@router.delete('/{game_id}')
async def delete_game(game_id: int, user: Annotated[dict, Depends(get_current_user)]):
    print(game_id)
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)

    if collection_name.find_one({"id": game_id}, {"_id": 0}):
        collection_name.delete_one({"id": game_id})
    else:
        raise HTTPException(status_code=404, detail="Not Found")

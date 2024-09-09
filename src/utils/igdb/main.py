import aiohttp
from async_lru import alru_cache

from src.config import AUTH_IGDB
from src.config import CLIENT_ID_IGDB

BASE_URL = "https://api.igdb.com"

headers = {
    "Client-ID": CLIENT_ID_IGDB,
    "Authorization": AUTH_IGDB,
}


@alru_cache
async def get_igdb_games(name: str) -> list:
    async with aiohttp.ClientSession(base_url=BASE_URL, headers=headers) as session:
        async with session.post("/v4/games",
                                data=f'fields cover.image_id, name; search "{name}";') as response:
            return await response.json()


@alru_cache
async def igdb_game_info(game_id: int) -> dict:
    async with aiohttp.ClientSession(base_url=BASE_URL, headers=headers) as session:
        async with session.post(f"/v4/games",
                                data=f"fields cover.image_id, name; where id={game_id};") as response:
            return await response.json()

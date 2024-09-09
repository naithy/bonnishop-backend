import aiohttp
from src.config import TG_TOKEN

BASE_URL = f"https://api.telegram.org"


async def send_message(chat_id: int, message: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage?text={message}&chat_id={str(chat_id)}") as response:
            return None

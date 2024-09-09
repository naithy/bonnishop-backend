import hashlib
from .schemas import OrderSchema
from .database import collection_name
from src.utils.telegram.main import send_message
from fastapi import WebSocket, WebSocketDisconnect
from fastapi import APIRouter, Request, HTTPException, status

from src.config import SHOP
from src.config import SECRET
from src.config import CURRENCY

router = APIRouter(prefix="/orders", tags=["Orders"])

WHITELISTED_IPS = [
    "127.0.0.1",
    "195.64.101.191",
    "194.124.49.173",
    "45.8.156.144",
    "5.180.194.179",
    "5.180.194.127",
    "2a0b:1580:5ad7:0dea:de47:10ae:ecbf:111a",
]


@router.post("/")
async def order_create(request: Request, order: OrderSchema):
    ip = str(request.client.host)

    signed_data = [SECRET, order.desc, CURRENCY, str(SHOP), order.payment_id, str(order.amount)]
    sign = hashlib.md5("|".join(signed_data).encode('utf-8')).hexdigest()

    if sign == order.sign:
        collection_name.insert_one(order.dict())

    if ip not in WHITELISTED_IPS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'IP {ip} is not allowed to access this resource.'
        )

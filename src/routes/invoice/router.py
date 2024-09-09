import time
import hashlib
from sqids import Sqids
from fastapi import APIRouter
from .schemas import InvoiceSchema
from fastapi.encoders import jsonable_encoder

from src.config import SHOP
from src.config import SECRET
from src.config import CURRENCY

router = APIRouter(prefix="/invoice", tags=["invoice"])

sqids = Sqids()


@router.post("/")
async def create_invoice(invoice: InvoiceSchema):
    data = jsonable_encoder(invoice)
    order_id = sqids.encode([int(data["user_id"]), int(float(data["amount"])), int(time.time())])
    data_to_sign = [str(int(float(data["amount"]))), str(order_id), str(SHOP), CURRENCY, data["desc"], SECRET]
    sign = hashlib.md5("|".join(data_to_sign).encode('utf-8')).hexdigest()

    data["desc"] = data["desc"].replace(" ", "%20")

    invoiceLink = f'https://payok.io/pay?amount={data["amount"]}&payment={order_id}&shop={SHOP}&desc={data["desc"]}&currency={CURRENCY}&sign={sign}&lang=RU&username={data["user_name"]}&userid={data["user_id"]}'

    return invoiceLink

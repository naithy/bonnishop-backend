from pydantic import BaseModel


class OrderSchema(BaseModel):
    payment_id: str
    shop: int
    amount: float
    profit: float
    desc: str
    currency: str
    currency_amount: float
    sign: str
    email: str
    date: str
    method: str
    custom: list
    underpayment: int

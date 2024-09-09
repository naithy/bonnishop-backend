from pydantic import BaseModel


class InvoiceSchema(BaseModel):
    amount: int
    desc: str
    user_name: str
    user_id: str

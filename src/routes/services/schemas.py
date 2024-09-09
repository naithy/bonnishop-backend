from pydantic import BaseModel, Field
from pydantic_collections import BaseCollectionModel


class ServiceSchema(BaseModel, extra="allow"):
    name: str
    image: str
    description: str = Field(default="")
    account: list = Field(default=[])
    subscription: list = Field(default=[])
    replenishment_balance: list = Field(default=[], alias='replenishmentBalance')
    change_region: list = Field(default=[], alias='changeRegion')
    gift_card: list = Field(default=[], alias='giftCard')
    donate: list = Field(default=[])
    boost: list = Field(default=[])
    battle_pass: list = Field(default=[], alias='battlePass')


class ServiceCollection(BaseCollectionModel[ServiceSchema]):
    pass

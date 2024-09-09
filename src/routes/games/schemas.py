from pydantic import BaseModel, Field
from pydantic_collections import BaseCollectionModel


class VariantGameSchema(BaseModel):
    method: str
    platform: str
    price: int
    provider: str
    region: str


class GameSchema(BaseModel):
    id: int
    name: str
    description: str = Field(default="")
    image_id: str = Field(alias='imageId')
    variants: list[VariantGameSchema]


class CollectionGameSchema(BaseCollectionModel[GameSchema]):
    pass

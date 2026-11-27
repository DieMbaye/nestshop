from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProductOut(BaseModel):
    """Un produit tel qu'il est renvoyé par l'API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: int
    stock: int


class OrderCreate(BaseModel):
    """Ce que la cliente envoie pour passer une commande."""

    model_config = ConfigDict(str_strip_whitespace=True)

    customer_name: str = Field(min_length=2, max_length=100)
    product_id: int = Field(gt=0)
    quantity: int = Field(gt=0, le=100)


class OrderOut(BaseModel):
    """Une commande telle qu'elle est renvoyée par l'API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_name: str
    product_id: int
    quantity: int
    total: int
    created_at: datetime
from pydantic import BaseModel, ConfigDict


class ProductOut(BaseModel):
    """Un produit tel qu'il est renvoyé par l'API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    price: int
    stock: int
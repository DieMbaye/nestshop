from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Product
from app.schemas import ProductOut

router = APIRouter(prefix="/api/products", tags=["Produits"])


@router.get("", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)):
    """Renvoie la liste de tous les produits."""
    return db.scalars(select(Product).order_by(Product.id)).all()
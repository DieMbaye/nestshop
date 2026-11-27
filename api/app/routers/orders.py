from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Order, Product
from app.schemas import OrderCreate, OrderOut

router = APIRouter(prefix="/api/orders", tags=["Commandes"])


@router.get("", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    """Renvoie toutes les commandes, de la plus récente à la plus ancienne."""
    return db.scalars(
        select(Order).order_by(Order.created_at.desc(), Order.id.desc())
    ).all()


@router.post("", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    """Crée une commande et diminue le stock du produit."""
    product = db.scalars(
        select(Product).where(Product.id == order_in.product_id).with_for_update()
    ).first()

    if product is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    if product.stock < order_in.quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Stock insuffisant : il reste {product.stock} article(s)",
        )

    product.stock -= order_in.quantity
    order = Order(
        customer_name=order_in.customer_name,
        product_id=product.id,
        quantity=order_in.quantity,
        total=product.price * order_in.quantity,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order
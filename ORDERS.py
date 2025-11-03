from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import database
from models.orders import Order
from models.products import Products
from schemas.orders import Order
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/Buyurtma_qilish")
async def create_order(form:Order, db:AsyncSession = Depends(database)):
    product = db.query(Products.Product).filter(Products.Product.id == Order.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Bunday mahsulot topilmadi !")

    total_price = Products.price * Order.quantity
    new_order = Order(
        user_id=Order.user_id,
        product_id=Order.product_id,
        quantity=Order.quantity,
        total_price=total_price
    )

    db.add(new_order)
    await db.commit()
    return "Buyurtma amalga oshdi !"

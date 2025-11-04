from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from db import database
from models.order_items import OrderItem
from schemas.order_items import SchemaOrderItem

order_item_router = APIRouter()


# 🔍 Barcha buyurtma elementlarini ko‘rish
@order_item_router.get("/Buyurtma_elementlarini_ko'rish")
async def get_all_order_items(db: AsyncSession = Depends(database)):
    result = await db.execute(select(OrderItem))
    return result.scalars().all()


# 🔍 Bitta order_item ni ID orqali ko‘rish
@order_item_router.get("/Buyurtma_elementini_id_bilan_ko'rish")
async def get_order_item(ident: int, db: AsyncSession = Depends(database)):
    result = await db.execute(select(OrderItem).where(OrderItem.id == ident))
    item = result.scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Buyurtma elementi topilmadi !")
    return item


# ➕ Buyurtmaga mahsulot qo‘shish
@order_item_router.post("/Buyurtmaga_mahsulot_qo'shish")
async def add_order_item(form: SchemaOrderItem, db: AsyncSession = Depends(database)):
    new_item = OrderItem(
        product_id=form.product_id,
        amount=form.amount,
        price=form.price,
        order_id=form.order_id
    )

    db.add(new_item)
    await db.commit()
    await db.refresh(new_item)
    return {"xabar": "Buyurtmaga mahsulot qo'shildi !", "id": new_item.id}


# ✏️ Buyurtma elementini tahrirlash
@order_item_router.put("/Buyurtma_elementini_tahrirlash")
async def update_order_item(ident: int, form: SchemaOrderItem, db: AsyncSession = Depends(database)):
    result = await db.execute(select(OrderItem).where(OrderItem.id == ident))
    item = result.scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Buyurtma elementi topilmadi !")

    await db.execute(
        update(OrderItem)
        .where(OrderItem.id == ident)
        .values(
            product_id=form.product_id,
            amount=form.amount,
            price=form.price,
            order_id=form.order_id
        )
    )
    await db.commit()
    return "Buyurtma elementi tahrirlandi !"


# ❌ Buyurtma elementini o‘chirish
@order_item_router.delete("/Buyurtma_elementini_o'chirish")
async def delete_order_item(ident: int, db: AsyncSession = Depends(database)):
    result = await db.execute(select(OrderItem).where(OrderItem.id == ident))
    item = result.scalar()
    if not item:
        raise HTTPException(status_code=404, detail="Buyurtma elementi topilmadi !")

    await db.execute(delete(OrderItem).where(OrderItem.id == ident))
    await db.commit()
    return "Buyurtma elementi o'chirildi !"

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from db import database
from models.products import Products
from schemas.products import SchemaProducts
from sqlalchemy.future import select
from sqlalchemy import update, delete

product_router = APIRouter()


@product_router.get("/Mahsulotlarni_ko'rish")   # barcha ma'lumotlarni ko'rish
async def get_all(db:AsyncSession = Depends(database)):
    result = await db.execute(select(Products))
    return result.scalars().all()


@product_router.get("/Mahsulotlarni_id_bilan_ko'rish")
async def get_product(ident:int = None, db:AsyncSession = Depends(database)):
    if ident:
        a = await db.execute(select(Products).where(Products.id == ident))
        return a.scalar()
    else:
        a = await db.execute(select(Products))
        return a.scalars().all()


@product_router.post("/Mahsulot_qo'shish")
async def add_product(form:SchemaProducts, db:AsyncSession = Depends(database)):
    product = Products(
        name = form.name,
        heading = form.heading,
        price = form.price,
        amount = form.amount,
        image = form.image
    )
    db.add(product)
    await db.commit()
    return "Mahsulot bazaga qo'shildi !"


# @product_router.post("/Mahsulotga_rasm_yuklash")       # bitmagan funksiya - hato
# async def product(file, db: AsyncSession, current_user : Users):
#
#     image_filename = await save_image(file)
#
#     async with db as session:
#         result = await session.execute(select(Products).filter(Products.id == current_user.id))
#         user = result.scalar()
#
#         if not user:
#             raise HTTPException(status_code=404, detail="User topilmadi")
#
#         user.image = image_filename
#         await session.commit()
#         return "Rasm yuklandi !"


@product_router.put("/Mahsulot_tahrirlash")
async def update_product(ident: int, form:SchemaProducts, db:AsyncSession = Depends(database)):
    result = await db.execute(select(Products).where(Products.id == ident))
    product = result.scalar()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found !")

    await db.execute(update(Products).where(Products.id == ident).values(
        name=form.name,
        heading=form.heading,
        price=form.price,
        amount=form.amount,
        image=form.image
    ))
    await db.commit()
    return "Mahsulot tahrirlandi !"


@product_router.delete("/Mahsulot_o'chirish")
async def delete_product(ident: int, db:AsyncSession = Depends(database)):
    result = await db.execute(select(Products).where(Products.id == ident))
    product = result.scalar()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found !")

    await db.execute(delete(Products).where(Products.id == ident))
    await db.commit()
    return "Mahsulot o'chirildi !"



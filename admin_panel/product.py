from sqladmin import ModelView
from models.products import Products

class ProductAdmin(ModelView, model = Products):
    column_list = ["id", "name", "heading", "price", "amount", "image"]
    name_plural = "Продукты"
    name = "Mahsulotlar"
    column_labels = {
        "id": "ID",
        "name": "Название",
        "heading": "Описание",
        "price": "Цена",
        "amount": "Количество",
        "image": "Изображение"
    }



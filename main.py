from fastapi import FastAPI
from routers.users import user_router
from routers.login import login_router
from starlette.middleware.cors import CORSMiddleware
from PRODUCT import product_router


app = FastAPI(docs_url="/", title="Sausage Factory API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

app.include_router(user_router, tags=["Profil"])
app.include_router(login_router)
app.include_router(product_router, tags=["Mahsulotlar"])

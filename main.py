from fastapi import FastAPI
from database.config import database
from apps.users.api import router as user_router
from apps.auth.api import router as auth_router
from apps.categories.api import router as category_router
from apps.variations.api import router as variation_router
from apps.products.api import router as product_router

app = FastAPI()

app.state.database = database

app.include_router(auth_router, prefix='/auth', tags=['Auth'])
app.include_router(user_router, prefix='/user', tags=['User'])
app.include_router(category_router, prefix='/category', tags=['Category'])
app.include_router(variation_router, prefix='/variation', tags=['Variation'])
app.include_router(product_router, prefix='/product', tags=['Product'])


@app.on_event("startup")
async def startup() -> None:
    database_ = app.state.database
    if not database_.is_connected:
        await database_.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    database_ = app.state.database
    if database_.is_connected:
        await database_.disconnect()

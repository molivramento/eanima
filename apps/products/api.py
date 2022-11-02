from fastapi import APIRouter

from apps.products.models import Product, Stock

router = APIRouter()


@router.get('/', response_model=Product)
async def products():
    return await Product.objects.all()


# @router.get('/stock', response_model=Stock)
# async def products():
#     return await Product.objects.select_related()
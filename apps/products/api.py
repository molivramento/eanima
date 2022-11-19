from uuid import UUID

from fastapi import APIRouter

from apps.categories.models import Category
from apps.variations.models import Variation
from apps.products.models import Product, ProductInventory
from apps.products.schema import RequestProducts, RequestStock

router = APIRouter()


@router.get('/', response_model=list[Product])
async def get_products():
    return await Product.objects.all()


@router.get('/id')
async def get_product(pk: UUID):
    return await Product.objects.get(id=pk)


@router.post('/create')
async def create_product(category_id: UUID, data: RequestProducts):
    category = await Category.objects.get(id=category_id)
    return await Product.objects.create(**data.dict(), category_id=category)


@router.put('/update')
async def update_product(pk_product: UUID, data: RequestProducts):
    product = await Product.objects.get(id=pk_product)
    return await product.update(**data.dict())


@router.delete('/delete')
async def delete_product(pk: UUID):
    product = await Product.objects.get(id=pk)
    return await product.delete()


@router.get('/stocks/', response_model=ProductInventory)
async def get_stocks():
    return await Product.objects.all()


@router.get('/stock/id', response_model=ProductInventory)
async def get_stock(pk: UUID):
    return await ProductInventory.objects.get(id=pk)


@router.post('/stock/create', response_model=ProductInventory)
async def create_stock(pk_product: UUID, pk_variation: UUID,  data: RequestStock):
    product = await Product.objects.get(id=pk_product)
    # TODO: Verificar se já existe no banco de dados algum stock com mesmo variante, subir error
    if pk_variation:
        variation = await Variation.objects.get(id=pk_variation)
    else:
        variation = None
    return await ProductInventory.objects.create(**data.dict(), product_id=product, variations=variation)

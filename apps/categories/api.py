from uuid import UUID
from fastapi import APIRouter
from apps.categories.models import Category
from apps.categories.schema import RequestCategory

router = APIRouter()


@router.get('/', response_model=list[Category])
async def get_categories():
    return await Category.objects.order_by('title').all()


@router.get('/subcategories/{parent}', response_model=list[Category])
async def get_categories(parent: UUID):
    return await Category.objects.filter(parent=parent).order_by('title').all()


@router.post('/create', response_model=Category)
async def create_category(category: RequestCategory):
    return await Category.objects.create(**category.dict())


@router.put('/update', response_model=Category)
async def update_category(pk: UUID, category: Category):
    update = await Category.objects.get(id=pk)
    return await update.update(**category.dict())


@router.delete('/delete/{pk}')
async def delete_category(pk: UUID):
    category = await Category.objects.get(id=pk)
    return await category.delete()


@router.get('/{pk}', response_model=Category)
async def get_category_by_id(pk: UUID):
    return await Category.objects.get(id=pk)

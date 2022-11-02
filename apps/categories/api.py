from uuid import UUID

from fastapi import APIRouter
from apps.categories.models import Category

router = APIRouter()


@router.get('/all', response_model=list[Category])
async def get_categories():
    return await Category.objects.all()


@router.get('/id', response_model=Category)
async def get_category_by_id(pk: UUID):
    return await Category.objects.get(id=pk)


@router.post('/create', response_model=Category)
async def create_category(category: Category):
    await category.save()
    return category


@router.put('/update', response_model=Category)
async def update_category(pk: UUID, category: Category):
    update = await Category.objects.get(id=pk)
    return await update.update(**category.dict())


@router.delete('/delete')
async def delete_category(pk: UUID):
    category = await Category.objects.get(id=pk)
    return await category.delete()

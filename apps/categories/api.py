from uuid import UUID, uuid4
from fastapi import APIRouter
from apps.categories.models import Category
from apps.categories.schema import RequestCategory

router = APIRouter()


@router.get('/', response_model=list[Category])
async def get_category():
    return await Category.objects.select_related('parent').all()


@router.get('/subCategories/{parent}', response_model=Category)
async def get_categories(parent: UUID):
    return await Category.objects.get_or_none(parent__id=parent)


@router.get('/{pk}', response_model=Category)
async def get_category_by_id(pk: UUID):
    return await Category.objects.get(id=pk)


@router.post('/create', response_model=Category)
async def create_category(category: RequestCategory, parent: UUID | None = None):
    if parent:
        category_parent = await Category.objects.get(id=parent)
        return await Category(**category.dict(), id=uuid4(), parent=category_parent).save()
    return await Category.objects.create(**category.dict())


@router.put('/update/{pk}', response_model=Category)
async def update_category(pk: UUID, category: Category):
    update = await Category.objects.get(id=pk)
    return await update.update(**category.dict())


@router.delete('/delete/{pk}')
async def delete_category(pk: UUID):
    category = await Category.objects.get(id=pk)
    return await category.delete()

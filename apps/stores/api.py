from uuid import UUID

from fastapi import APIRouter

from apps.stores.models import Store
from apps.stores.schema import CreateStore

router = APIRouter()


@router.get('/', response_model=list[Store])
async def stores():
    return await Store.objects.all()


@router.get('/{pk}', response_model=Store)
async def get_store(pk: UUID):
    return await Store.objects.get(id=pk)


@router.post('/create', response_model=Store)
async def create_store(store: CreateStore):
    return await Store.objects.create(**store.dict())


@router.put('/update/{pk}')
async def update_store(pk: UUID, att: CreateStore):
    store = await Store.objects.get(id=pk)
    return await store.update(**att.dict())


@router.delete('/delete/{pk}')
async def delete_store(pk: UUID):
    store = await Store.objects.get(id=pk)
    await store.delete()
    return {'store': store, 'message': 'deleted'}

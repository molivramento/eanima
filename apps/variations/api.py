from uuid import UUID
from fastapi import APIRouter
from apps.variations.models import Variation, Option
from apps.variations.schema import RequestVariationOption, RequestVariation

router = APIRouter()


@router.get('/', response_model=list[Variation])
async def variations():
    return await Variation.objects.all()


@router.get('/{pk}', response_model=Variation)
async def get_variation(pk: UUID):
    return await Variation.objects.get(id=pk)


@router.post('/create', response_model=Variation)
async def create_variation(data: RequestVariation):
    return await Variation.objects.create(**data.dict())


@router.put('/update/{pk}', response_model=Variation)
async def update_variation(pk: UUID, data: RequestVariation):
    update = await Variation.objects.get(id=pk)
    return await update.update(**data.dict())


@router.delete('/delete/{pk}')
async def delete_variation(pk: UUID):
    return await Variation.objects.delete(id=pk)


@router.get('/variation-options', response_model=list[Variation], response_model_exclude={
    'variationoptions': {
        'variation': ...}})
async def get_options_of_variation(pk: UUID):
    return await Variation.objects.select_related('variationoptions').filter(id=pk).all()


@router.post('/option/create', response_model=Option)
async def create_variation(pk: UUID, data: RequestVariationOption):
    get_variation = await Variation.objects.get(id=pk)
    return await Option.objects.create(**data.dict(), variation=get_variation)


@router.put('/option/update', response_model=Option)
async def update_variation(pk: UUID, data: RequestVariationOption):
    update = await Option.objects.get(id=pk)
    return await update.update(**data.dict())

import ormar
from db import BaseMeta
from ormar import pre_save
from uuid import UUID, uuid4


class Store(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'stores'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    name: str = ormar.String(max_length=128, nullable=True)
    cep: str = ormar.String(max_length=12, nullable=True)
    address: str = ormar.String(max_length=255, nullable=True)
    city: str = ormar.String(max_length=128, nullable=True)
    uf: str = ormar.String(max_length=2, nullable=True)
    longitude: str = ormar.String(max_length=64, default=None, nullable=True)
    latitude: str = ormar.String(max_length=64, default=None, nullable=True)


@pre_save([Store])
async def create_uuid(sender, instance, **kwargs):
    instance.id = uuid4()

from uuid import UUID

import ormar

from db import BaseMeta


class Store(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'stores'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    name: str = ormar.String(max_length=128)
    cep: str = ormar.String(max_length=12)
    address: str = ormar.String(max_length=255)
    city: str = ormar.String(max_length=128)
    uf: str = ormar.String(max_length=2)
    longitude: str = ormar.String(max_length=64, default=None)
    latitude: str = ormar.String(max_length=64, default=None)

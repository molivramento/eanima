import ormar

from typing import Optional
from uuid import UUID, uuid4

from ormar import pre_save

from db import BaseMeta


class Variation(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'variations'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    name: str = ormar.String(max_length=128, nullable=True)
    tag: str = ormar.String(max_length=128, nullable=True)


# TODO: add image
class Option(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'options'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    variation: Optional[Variation] = ormar.ForeignKey(Variation, nullable=True)
    value: str = ormar.String(max_length=128, default=None)
    unit: str = ormar.String(max_length=32, nullable=True)


@pre_save([Option, Variation])
async def create_uuid(sender, instance, **kwargs):
    instance.id = uuid4()

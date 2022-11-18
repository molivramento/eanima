from datetime import datetime

import ormar
from uuid import UUID, uuid4

from ormar import pre_save

from db import BaseMeta


class Category(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'categories'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    name: str = ormar.String(max_length=128)
    slug: str = ormar.String(max_length=128, nullable=True)
    description: str = ormar.Text(nullable=True)
    active: bool = ormar.Boolean(default=True)
    parent: UUID = ormar.UUID(nullable=True)
    starting: datetime = ormar.DateTime(default=datetime.utcnow)
    ending: datetime = ormar.DateTime(default=None, nullable=True)
    discount: float = ormar.Decimal(decimal_places=5, max_digits=6, default=1)
    starting_discount: datetime = ormar.DateTime(default=None, nullable=True)
    ending_discount: datetime = ormar.DateTime(default=None, nullable=True)
    meta_title: str = ormar.String(max_length=70, nullable=True, default=True)
    meta_description: str = ormar.String(max_length=160, nullable=True, default=None)
    meta_keywords: str = ormar.Text(nullable=True, default=None)


@pre_save(Category)
async def create_uuid(sender, instance, **kwargs):
    instance.id = uuid4()

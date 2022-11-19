import ormar
from pydantic.typing import ForwardRef

from db import BaseMeta
from ormar import pre_save
from uuid import UUID, uuid4
from datetime import datetime


CategoryRef = ForwardRef('Category')


class Category(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'categories'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    name: str = ormar.String(max_length=128)
    slug: str = ormar.String(max_length=128, nullable=True)
    description: str = ormar.Text(nullable=True, default=None)
    active: bool = ormar.Boolean(default=True)
    parent: CategoryRef = ormar.ForeignKey(CategoryRef, related_name='parent', nullable=True)
    starting: datetime = ormar.DateTime(default=datetime.utcnow)
    ending: datetime = ormar.DateTime(nullable=True, default=None)
    discount: float = ormar.Decimal(decimal_places=5, max_digits=6, default=1.00)
    starting_discount: datetime = ormar.DateTime(nullable=True, default=None)
    ending_discount: datetime = ormar.DateTime(nullable=True, default=None)
    meta_title: str = ormar.String(max_length=70, nullable=True, default=None)
    meta_description: str = ormar.String(max_length=160, nullable=True, default=None)
    meta_keywords: str = ormar.Text(nullable=True, default=None)


Category.update_forward_refs()


@pre_save([Category])
async def create_uuid(sender, instance, **kwargs):
    instance.id = uuid4()


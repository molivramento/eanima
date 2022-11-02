import ormar
from ormar import pre_save
from uuid import UUID, uuid4
from database.config import BaseMeta


class Category(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'categories'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    title: str = ormar.String(max_length=128)
    slug: str = ormar.String(max_length=128, nullable=True)
    description: str = ormar.Text(nullable=True)
    active: bool = ormar.Boolean(default=True)
    parent_id: UUID = ormar.UUID(nullable=True)


@pre_save(Category)
async def create_uuid(sender, instance, **kwargs):
    instance.id = uuid4()

import ormar
from ormar import pre_save
from uuid import UUID, uuid4
from datetime import datetime
from database.config import BaseMeta


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'users'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    email: str = ormar.String(unique=True, max_length=125)
    password: str = ormar.String(max_length=128, nullable=True)
    is_active: bool = ormar.Boolean(default=True)
    disabled: bool = ormar.Boolean(default=False)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    last_login: datetime = ormar.DateTime(default=datetime.utcnow)


@pre_save(User)
async def create_uuid(sender, instance, **kwargs):
    instance.id = uuid4()


@pre_save(User)
async def create_at(sender, instance, **kwargs):
    instance.created_at = datetime.now()

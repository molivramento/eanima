import ormar
from db import BaseMeta
from ormar import pre_save
from uuid import UUID, uuid4
from datetime import datetime


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'users'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    email: str = ormar.String(unique=True, max_length=125)
    password: str = ormar.String(max_length=128, nullable=True)
    disabled: bool = ormar.Boolean(default=False)
    verified: bool = ormar.Boolean(default=False)
    is_admin: bool = ormar.Boolean(default=False)
    created: datetime = ormar.DateTime(default=datetime.utcnow)
    last_login: datetime = ormar.DateTime(default=None, nullable=True)


@pre_save([User])
async def create_uuid(sender, instance, **kwargs):
    instance.id = uuid4()

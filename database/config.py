import datetime
from uuid import UUID

import ormar
import databases
import sqlalchemy

database = databases.Database('sqlite:///db.sqlite')
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    database = database
    metadata = metadata


class AuditMixin(ormar.Model):
    class Meta:
        abstract = True

    created_by: UUID = ormar.UUID(nullable=True)
    updated_by: UUID = ormar.UUID(nullable=True)


class DateFieldsMixin(ormar.Model):
    class Meta:
        abstract = True
        metadata = metadata
        database = database

    created_date: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now,
        nullable=True
    )
    updated_date: datetime.datetime = ormar.DateTime(
        default=datetime.datetime.now,
        nullable=True
    )

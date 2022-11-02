from typing import Optional
from uuid import UUID, uuid4

import ormar
from ormar import pre_save

from database.config import AuditMixin, DateFieldsMixin, BaseMeta


class Variation(AuditMixin, DateFieldsMixin):
    class Meta(ormar.ModelMeta):
        tablename = 'variations'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    name: str = ormar.String(max_length=128, nullable=True)


# TODO: add image
class VariationOption(AuditMixin, DateFieldsMixin):
    class Meta(ormar.ModelMeta):
        tablename = 'variation_options'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    variation: Optional[Variation] = ormar.ForeignKey(Variation, nullable=True)
    value: str = ormar.String(max_length=128, default=None)


@pre_save([Variation, VariationOption])
async def create_uuid(sender, instance, **kwargs):
    instance.id = uuid4()

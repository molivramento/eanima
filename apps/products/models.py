import ormar

from ormar import pre_save
from typing import Optional
from uuid import UUID, uuid4
from database.config import BaseMeta, DateFieldsMixin, AuditMixin

from apps.categories.models import Category
from apps.variations.models import Variation


# TODO: Add image!
class Product(DateFieldsMixin, AuditMixin):
    class Meta(ormar.ModelMeta):
        tablename = 'products'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    category_id: Optional[Category] = ormar.ForeignKey(Category)
    title: str = ormar.String(max_length=255)
    slug: str = ormar.String(max_length=255, unique=True)
    short_description: str = ormar.Text(nullable=True)
    long_description: str = ormar.Text(nullable=True)


class Stock(DateFieldsMixin, AuditMixin):
    class Meta(ormar.ModelMeta):
        tablename = 'stocks'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    product_id: Optional[Product] = ormar.ForeignKey(Product, nullable=True)
    variations: Optional[list[Variation]] = ormar.ManyToMany(Variation, nullable=True)
    sku: str = ormar.String(max_length=128)
    amount: int = ormar.Integer(default=0)
    price: float = ormar.Decimal(max_digits=10, decimal_places=2)
    active: bool = ormar.Boolean(default=True)
    site: bool = ormar.Boolean(default=True)
    discount_price: float = ormar.Decimal(max_digits=10, default=0.00, nullable=True, decimal_places=2)


@pre_save([Stock, Product])
async def create_uuid(sender, instance, **kwargs):
    instance.id = uuid4()

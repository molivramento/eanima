from datetime import datetime

import ormar

from uuid import UUID, uuid4
from typing import Optional

from ormar import pre_save

from db import BaseMeta

from apps.stores.models import Store
from apps.categories.models import Category
from apps.variations.models import Variation


# TODO: Add images!
class Product(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'products'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    categories: Optional[list[Category]] = ormar.ForeignKey(Category, nullable=True)
    title: str = ormar.String(max_length=255, nullable=True)
    slug: str = ormar.String(max_length=255, unique=True)
    description: str = ormar.Text(nullable=True)
    site: bool = ormar.Boolean(default=True)
    active: bool = ormar.Boolean(default=True)
    meta_title: str = ormar.String(max_length=70, nullable=True, default=True)
    meta_description: str = ormar.String(max_length=160, nullable=True, default=None)
    meta_keywords: str = ormar.Text(nullable=True, default=None)


class ProductInventory(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'product_inventory'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    store: Optional[Store] = ormar.ForeignKey(Store, nullable=True)
    ean: str = ormar.String(max_length=64, unique=True)
    sku: str = ormar.String(max_length=128, unique=True)
    amount: int = ormar.Integer(nullable=True)
    cost: float = ormar.Decimal(max_digits=10, decimal_places=2, default=None)
    price: float = ormar.Decimal(max_digits=10, decimal_places=2, default=None)
    price_web: float = ormar.Decimal(max_digits=10, decimal_places=2, default=None)
    price_b2b: float = ormar.Decimal(max_digits=10, decimal_places=2, default=None)
    discount: float = ormar.Decimal(decimal_places=2, max_digits=3, default=None)
    starting_discount: datetime = ormar.DateTime(default=None, nullable=True)
    ending_discount: datetime = ormar.DateTime(default=None, nullable=True)


class ProductOption(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'product_options'

    id: UUID = ormar.UUID(primary_key=True, nullable=True)
    products: Optional[ProductInventory] = ormar.ForeignKey(ProductInventory)
    variation: Optional[list[Variation]] = ormar.ManyToMany(Variation)


@pre_save([Product, ProductInventory, ProductOption])
async def create_uuid(sender, instance, **kwargs):
    instance.id = uuid4()

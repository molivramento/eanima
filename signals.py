from uuid import uuid4
from ormar import pre_save
from apps.users.models import User
from apps.stores.models import Store
from apps.categories.models import Category
from apps.variations.models import Variation, Option
from apps.products.models import Product, ProductInventory

from apps.categories.models import Category

RequestCategory = Category.get_pydantic(
    exclude={
        'id': ...,
        'products': ...,
        'description': ...,
        'active': ...
    }
)

from apps.categories.models import Category

RequestCategory = Category.get_pydantic(
    exclude={
        'id': ...,
        'products': ...,
        'description': ...,
        'active': ...,
        'starting': ...,
        'ending': ...,
        'discount': ...,
        'starting_discount': ...,
        'ending_discount': ...,
        'meta_title': ...,
        'meta_description': ...,
        'meta_keywords': ...,
        'parent': ...
    }
)

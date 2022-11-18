from apps.products.models import Product, ProductInventory

RequestProducts = Product.get_pydantic(
    exclude={
        'created_date': ...,
        'updated_date': ...,
        'created_by': ...,
        'updated_by': ...,
        'id': ...,
        'category_id': ...,
        'stocks': ...
    }
)

RequestStock = ProductInventory.get_pydantic(
    exclude={
        'created_date': ...,
        'updated_date': ...,
        'created_by': ...,
        'updated_by': ...,
        'id': ...,
        'product_id': ...,
        'variations': ...
    }
)

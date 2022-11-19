from apps.stores.models import Store

CreateStore = Store.get_pydantic(
    exclude={
        'id': ...,
        'productinventorys': ...
    }
)

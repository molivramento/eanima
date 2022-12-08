from apps.variations.models import Option, Variation

RequestVariation = Variation.get_pydantic(
    exclude={
        'id': ...,
        'options': ...,
        'productoptions': ...
    }
)

RequestVariationOption = Option.get_pydantic(
    exclude={
        'id': ...,
        'variation': ...
    }
)

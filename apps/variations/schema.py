from apps.variations.models import VariationOption, Variation

RequestVariation = Variation.get_pydantic(
    exclude={
        'id': ...,
        'created_by': ...,
        'updated_by': ...,
        'created_date': ...,
        'updated_date': ...,
        'variationoptions': ...
    }
)

RequestVariationOption = VariationOption.get_pydantic(
    exclude={
        'id': ...,
        'created_by': ...,
        'updated_by': ...,
        'created_date': ...,
        'updated_date': ...,
        'variation': ...
    }
)
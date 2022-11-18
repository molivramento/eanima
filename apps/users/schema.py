from apps.users.models import User

RequestUser = User.get_pydantic(
    exclude={
        'id': ...,
        'verified': ...,
        'disabled': ...,
        'created': ...,
        'last_login': ...
    }
)

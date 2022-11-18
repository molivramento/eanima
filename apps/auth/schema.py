from pydantic import BaseModel

from apps.users.models import User


ResponseUser = User.get_pydantic(
    exclude={
        'password'
    }
)


RequestLastLogin = User.get_pydantic(
    include={
        'last_login': ...
    }
)

RequestWithoutLastLogin = User.get_pydantic(
    exclude={
        'last_login': ...
    }
)

RequestLogin = User.get_pydantic(
    include={
        'username': ...,
        'password': ...
    }
)


class ResponseToken(BaseModel):
    token: str

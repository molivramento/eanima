from fastapi import APIRouter

from apps.auth.utils import get_user, get_password_hash
from apps.users.models import User

router = APIRouter()


@router.post('/register', response_model=User, response_model_exclude={'password'})
async def register(user: User):
    password_hash = get_password_hash(user.password)
    user = await User.objects.create(email=user.email, password=password_hash)
    return user


@router.get('/email', response_model=User, response_model_exclude={'password'})
async def get_user_by_email(email: str):
    return await get_user(email=email)

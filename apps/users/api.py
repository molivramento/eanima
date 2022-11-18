from fastapi import APIRouter, Depends, HTTPException, status

from apps.users.schema import RequestUser
from apps.users.models import User
from apps.auth.utils import get_user, get_hashed_password, get_current_active_user

router = APIRouter()


@router.get('/', response_model=list[User], response_model_exclude={'password'})
async def users():
    return await User.objects.all()


@router.post('/register', response_model=User, response_model_exclude={'password'})
async def register(user: RequestUser):
    verify_user = await User.objects.get_or_none(username=user.username)
    if verify_user is not None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='This user already exist!')
    password_hash = get_hashed_password(user.password)
    return await User.objects.create(email=user.email, password=password_hash)


@router.get('/{email}', response_model=User, response_model_exclude={'password'})
async def get_user_by_email(email: str):
    return await get_user(username=email)

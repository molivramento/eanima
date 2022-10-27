from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .utils import authenticate_user, create_access_token, get_current_user, get_current_active_user
from ..users.models import User

router = APIRouter()


@router.post('/token')
async def login_for_access_token(credentials: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect email or password'
        )
    access_token = create_access_token(
        data={'email': user.email}
    )
    return {'access_token': access_token, 'token_type': 'Bearer'}


@router.get('/me', response_model=User, response_model_exclude={'password'})
async def me(current_user: User = Depends(get_current_active_user)):
    return current_user

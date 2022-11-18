from .deps import JWTBearer
from .schema import RequestLogin, ResponseUser
from fastapi import APIRouter, Depends, HTTPException, status, Request
from .utils import authenticate_user, encode_token, encode_refresh_token, decode_refresh_token, decode_token, uuid_auth

from ..users.models import User

router = APIRouter()


@router.post('/login')
async def get_token(data: RequestLogin):
    user = await authenticate_user(data)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='User does not exist!')
    access_token = encode_token(data={'id': str(user.id), 'username': user.username})
    rf = encode_refresh_token(data={'id': str(user.id), 'username': user.username})
    return {'access_token': access_token, 'refresh_token': rf, 'user': user}


@router.post('/refreshToken')
async def refresh_token(request: Request):
    rf = request.headers.get('authorization').split()[1]
    return decode_refresh_token(rf)


@router.get('/me', response_model=ResponseUser, dependencies=[Depends(JWTBearer())])
async def me(request: Request):
    return await User.objects.get(id=uuid_auth(request))


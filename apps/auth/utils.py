import os
import time
from datetime import datetime, timedelta
from uuid import UUID

from dotenv import load_dotenv
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import status, HTTPException, Depends, Request

from apps.auth.schema import RequestLogin, RequestLastLogin, RequestWithoutLastLogin, ResponseUser
from apps.users.models import User

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
REFRESH_SECRET_KEY = os.getenv('REFRESH_SECRET_KEY')
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 1
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = HTTPBearer()


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


async def get_user(username: str):
    user = await User.objects.get_or_none(username=username)
    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='This user does not exist'
        )
    elif user.disabled:
        raise HTTPException(
            status.HTTP_423_LOCKED,
            detail='User disabled!'
        )
    return user


async def authenticate_user(data: RequestLogin):
    user = await get_user(data.username)
    if user is None:
        return False
    if not verify_password(password=data.password, hashed_password=user.password):
        return False
    return user


def to_encode(data: dict, key: str, expires: int, expires_delta: timedelta | None = None):
    enc = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=expires)
    enc.update({'exp': expire})
    return jwt.encode(enc, key, ALGORITHM)


def encode_token(data: dict, expires_delta: timedelta | None = None):
    return to_encode(
        data=data,
        key=SECRET_KEY,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES,
        expires_delta=expires_delta
    )


def encode_refresh_token(data: dict, expires_delta: timedelta = None):
    return to_encode(
        data=data,
        key=REFRESH_SECRET_KEY,
        expires=REFRESH_TOKEN_EXPIRE_MINUTES,
        expires_delta=expires_delta
    )


def decode_token(token: str):
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if float(decoded_token['exp']) > time.time():
        return decoded_token
    else:
        return None


def decode_refresh_token(refresh: str):
    decoded_token = jwt.decode(refresh, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    print(decoded_token)
    if float(decoded_token['exp']) > time.time():
        return {
            'access_token': encode_token(data={'id': str(decoded_token['id']), 'username': decoded_token['username']}),
            'refresh_token': encode_refresh_token(data={'id': str(decoded_token['id']), 'username': decoded_token['username']})
        }
    else:
        return None


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail='Cold not validate credentials'
    )
    try:
        payload = decode_token(token)
        username: str = payload.get('username')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Inactive user')
    return current_user


async def update_last_login(user: User):
    last_login = RequestLastLogin(last_login=datetime.utcnow())
    without_last_login = RequestWithoutLastLogin(**user.dict())
    await user.update(**without_last_login.dict(), **last_login.dict())


def uuid_auth(request: Request):
    token = request.headers.get('authorization').split()[1]
    decode = decode_token(token)
    return UUID(decode['id'])
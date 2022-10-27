import os
from jose import jwt, JWTError
from dotenv import load_dotenv
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException, Depends

from apps.users.models import User

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


async def get_user(email: str):
    user = await User.objects.get_or_none(email=email)
    if user is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='This user does not exist'
        )
    elif not user.is_active:
        raise HTTPException(
            status.HTTP_423_LOCKED,
            detail='User disabled!'
        )
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)


async def authenticate_user(email: str, password: str):
    user = await get_user(email=email)
    if user is None:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail='Cold not validate credentials'
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get('email')
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await get_user(email=email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

import jwt

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.models import Model

from .const import JWT_SECRET


router = APIRouter()
https://www.youtube.com/watch?v=vVjWeLVv97c

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(60)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)


user_pydantic = pydantic_model_creator(User, name='User')
user_in_pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)
oath2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def authenticate_user(username: str, password: str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


async def get_current_user(token: str = Depends(oath2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    return await user_pydantic.from_tortoise_orm(user)


async def get_users(token: str = Depends(oath2_scheme)):
    try:
        # payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        users = await User.all()
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    return users


@router.post('/token', tags=["users"])
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return {'error': 'invalid credentials'}
    user_obj = await user_pydantic.from_tortoise_orm(user)
    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


@router.post('/user', response_model=user_pydantic, tags=["users"])
async def create_user(user: user_in_pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await user_pydantic.from_tortoise_orm(user_obj)


@router.get('/users', tags=["users"])
async def get_users(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        return {'error': 'invalid credentials'}
    return await user_pydantic.from_queryset(User.all())


@router.get('/user/me', response_model=user_pydantic, tags=["users"])
async def get_user(user: user_pydantic = Depends(get_current_user)):
    return user

from datetime import time
from sys import prefix

from fastapi.params import Depends, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from starlette import status

from api_v1.users.schemas import UserSchema
from auth import utils as auth_utils
from fastapi import APIRouter, HTTPException

from jwt.exceptions import DecodeError


http_bearer = HTTPBearer()

class TokenInfo(BaseModel):
    access_token: str
    token_type: str

router = APIRouter(prefix='/jwt', tags=['JWT'])

admin = UserSchema(
    username='admin',
    password=auth_utils.hash_password('qwerty'),
    email='admin@gmail.com',
)

redlikeroses = UserSchema(
    username='redlikeroses',
    password=auth_utils.hash_password('secret'),
)

users_db: dict[str, UserSchema] = {
    admin.username: admin,
    redlikeroses.username: redlikeroses,
}


def validate_auth_user(
        username: str = Form(),
        password: str = Form(),

):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='invalid username or password',
    )

    user = users_db.get(username)
    if not user:
        raise unauthed_exc
    if not auth_utils.validate_passwords(password, user.password):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='user inactive',
        )

    return user



@router.post('/login')
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user)
):
    jwt_payload = {
        'sub': user.username,
        'username': user.username,
        'email': user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload,)
    return TokenInfo(
        access_token=token,
        token_type='Bearer',
    )

def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> UserSchema:
    try:
        token = credentials.credentials
        payload = auth_utils.decode_jwt(token)
    except DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'decode token error: {e}',
        )
    return payload


def get_current_auth_user_with_jwt(
        payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    username: str = payload.get('sub')
    user = users_db.get(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='invalid token',
        )
    return user


def get_current_active_auth_user_with_jwt(
        user: UserSchema = Depends(get_current_auth_user_with_jwt)
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='user inactive',
    )


@router.get('/users/me')
def auth_user_check_self_info(
        user: UserSchema = Depends(get_current_active_auth_user_with_jwt)
):
    return {
        'username': user.username,
        'email': user.email,
    }


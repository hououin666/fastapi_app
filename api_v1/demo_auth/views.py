import uuid
from time import time
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, Header
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED

router = APIRouter(prefix='/demo-auth', tags=['Demo Auth'])

security = HTTPBasic()


@router.get('/basic-auth')
def demo_basic_auth_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {
        'message': 'Hi!',
        'username': credentials.username,
        'password': credentials.password,
    }


usernames_to_passwords = {
    'admin': 'admin',
    'username': 'username',
}

static_auth_token_to_username = {
    'a0333b0c09023deac669f0b4b109ac7': 'admin',
    '5dddc1090b5a1d8ef175cc507ab7c5aae': 'hehe',
}


def get_auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username not in usernames_to_passwords:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    if credentials.password != usernames_to_passwords[credentials.username]:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    return credentials.username


def get_username_by_static_auth_token(
        static_token: str = Header(alias='x-static-auth-token')
) -> str:
    if static_token not in static_auth_token_to_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='token invalid',
        )
    return static_auth_token_to_username[static_token]



@router.get('/basic-auth-username')
def demo_basic_auth_username(auth_username: str = Depends(get_auth_user_username)):
    return {
        'message': f'Hi, {auth_username}!',
        'username': auth_username,
    }


@router.get('/some-http-header-auth')
def demo_auth_some_http_header(
        username: str = Depends(get_username_by_static_auth_token)
):
    return {
        'message': f'Hi, {username}',
        'username': username,
    }


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = 'web-app-session-id'


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)) -> dict:
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='not authenticated',
        )
    return COOKIES[session_id]


@router.post('/login-cookie/')
def demo_auth_logit_set_cookie(
        response: Response,
        auth_username: str = Depends(get_auth_user_username),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        'username': auth_username,
        'login_at': time(),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {'result': 'ok'}


@router.get('/check-cookie/')
def demo_auth_check_cookie(
    user_session_data: dict = Depends(get_session_data),
):
    username = user_session_data['username']
    return {'result': f'Hi, {username}',
            **user_session_data}





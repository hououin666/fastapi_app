from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
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


def get_auth_user_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username not in usernames_to_passwords:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    if credentials.password != usernames_to_passwords[credentials.username]:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail='invalid username or password')
    return credentials.username


@router.get('/basic-auth-username')
def demo_basic_auth_username(auth_username: str = Depends(get_auth_user_username)):
    return {
        'message': f'Hi, {auth_username}!',
        'username': auth_username,
    }
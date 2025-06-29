from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials, HTTPBasic

router = APIRouter(prefix='/demo-auth', tags=['Demo Auth'])

security = HTTPBasic()


@router.get('/basic-auth')
def demo_basic_auth_credentials(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    return {
        'message': 'Hi!',
        'username': credentials.username,
        'password': credentials.password,
    }
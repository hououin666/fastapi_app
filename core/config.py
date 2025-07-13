from pathlib import Path

from pydantic import BaseModel
from pydantic.v1 import BaseSettings

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    db_url: str = 'sqlite+aiosqlite:///db.sqlite3'
    db_echo: bool = False

    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()


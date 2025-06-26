from sys import prefix
from typing import List

from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(tags=['Movies'],prefix='/movies')


fake_movie_db = [
    {
        'name': 'Star Wars: Episode IX',
        'plot': 'The surviving members of the resistance face the First Order once again.',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Daisy Ridley', 'Adam Driver'],
    },
    {
        'name': 'Star Wars: Episode IX',
        'plot': 'The surviving members of the resistance face the First Order once again.',
        'genres': ['Action', 'Adventure', 'Fantasy'],
        'casts': ['Daisy Ridley', 'Adam Driver'],
    }
]

class Movie(BaseModel):
    name:str
    plot:str
    genres: List[str]
    casts: List[str]

@router.get('', response_model=List[Movie])
async def movies():
    return fake_movie_db
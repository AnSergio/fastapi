from fastapi import FastAPI
from pydantic import BaseModel


class Song(BaseModel):
    id: str
    title: str
    artist: str
    url: str

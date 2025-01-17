from fastapi import Depends, FastAPI
from sqlmodel import select
from sqlmodel import Session
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import init_db, get_session
from app.models import Song, SongCreate

app = FastAPI()

# @app.on_event("startup")
# def on_startup():
#     init_db()

@app.get("/ping")
async def pong():
    return {"ping": "pong!"}

@app.get("/songs", response_model=list[Song])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = session.execute(select(Song))
    songs = result.scalars().all()
    return [Song(name=song.name, artist=song.artist, year=song.year, id=song.id) for song in songs]

@app.post("/songs")
def add_song(song: SongCreate, session: AsyncSession = Depends(get_session)):
    song = Song(name=song.name, artist=song.artist, year=song.year)
    session.add(song)
    session.commit()
    session.refresh(song)
    return song

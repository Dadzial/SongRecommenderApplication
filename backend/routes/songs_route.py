from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..database.db_init import get_db
from ..services import songs_service
from ..schemas.songs_schema import SongResponse

router = APIRouter(prefix="/songs", tags=["songs"])

@router.get("/search/{name}", response_model=List[SongResponse])
def search_songs(name: str, db: Session = Depends(get_db)):
    songs = songs_service.get_songs_by_name(db, name)
    if not songs:
        raise HTTPException(status_code=404, detail="No songs found with that name")
    return songs

@router.get("/{track_id}", response_model=SongResponse)
def get_song_details(track_id: str, db: Session = Depends(get_db)):
    song = songs_service.get_song_by_track_id(db, track_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song

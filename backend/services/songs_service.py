from sqlalchemy.orm import Session
from ..database.tables.songs import Song

def get_songs_by_name(db: Session, name: str, limit: int = 10):
    return db.query(Song).filter(Song.track_name.ilike(f"%{name}%")).limit(limit).all()

def get_song_by_track_id(db: Session, track_id: str):
    return db.query(Song).filter(Song.track_id == track_id).first()

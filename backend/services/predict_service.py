import numpy as np
from sqlalchemy.orm import Session
from ..database.tables.songs import Song
from ..ml.ml_loader import ml_loader

def get_recommendations(db: Session, track_ids: list[str], n_neighbors: int = 10):
    if not ml_loader.model:
        return []

    input_songs = db.query(Song).filter(Song.track_id.in_(track_ids)).all()
    if not input_songs:
        return []


    feature_cols = [
        'popularity', 'duration_ms', 'danceability', 'energy', 'key', 
        'loudness', 'mode', 'speechiness', 'acousticness', 
        'instrumentalness', 'liveness', 'valence', 'tempo', 'time_signature'
    ]

    features = []
    for song in input_songs:
        song_features = [getattr(song, col) for col in feature_cols]
        features.append(song_features)

    user_profile = np.mean(features, axis=0).reshape(1, -1)

    distances, indices = ml_loader.model.kneighbors(user_profile, n_neighbors=n_neighbors + len(track_ids))


    recommended_indices = indices[0]

    final_indices = [idx + 1 for idx in recommended_indices]
    
    recommended_songs = db.query(Song).filter(Song.id.in_(final_indices)).all()

    result = [s for s in recommended_songs if s.track_id not in track_ids][:n_neighbors]

    return result

import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from ..database.tables.songs import Song
from ..ml.ml_loader import ml_loader

def get_recommendations(db: Session, track_ids: list[str], n_neighbors: int = 5):
    if not ml_loader.model:
        return []


    input_songs = db.query(Song).filter(Song.track_id.in_(track_ids)).all()
    if not input_songs:
        print("Error: No songs found for the provided track IDs.")
        return []


    feature_cols = [
        'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 
        'instrumentalness', 'liveness', 'valence', 'tempo'
    ]

    features_list = []
    for song in input_songs:
        song_features = [float(getattr(song, col)) for col in feature_cols]
        features_list.append(song_features)

    user_profile = np.mean(features_list, axis=0).reshape(1, -1)

    user_profile_df = pd.DataFrame(user_profile, columns=feature_cols)

    distances, indices = ml_loader.model.kneighbors(user_profile_df, n_neighbors=n_neighbors + len(track_ids))

    recommended_indices = indices[0].tolist()
    final_db_ids = [int(idx) + 1 for idx in recommended_indices]
    
    recommended_songs = db.query(Song).filter(Song.id.in_(final_db_ids)).all()

    result = [s for s in recommended_songs if s.track_id not in track_ids][:n_neighbors]
    
    print(f"Sukcess: {len(result)}.")
    return result

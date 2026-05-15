import numpy as np
import pandas as pd
from sqlalchemy.orm import Session
from ..database.tables.songs import Song
from ..ml.ml_loader import ml_loader

GENRE_CATEGORIES = [
    'genre_acoustic', 'genre_classical', 'genre_electronic', 'genre_hip-hop',
    'genre_inne', 'genre_jazz-soul', 'genre_latin', 'genre_metal',
    'genre_pop', 'genre_reggae', 'genre_rock', 'genre_world'
]

GENRE_MAP = {
    'acoustic': 'genre_acoustic',
    'afrobeat': 'genre_world',
    'alt-rock': 'genre_rock',
    'alternative': 'genre_rock',
    'ambient': 'genre_electronic',
    'black-metal': 'genre_metal',
    'bluegrass': 'genre_inne',
    'blues': 'genre_jazz-soul',
    'brazil': 'genre_latin',
    'breakbeat': 'genre_electronic',
    'british': 'genre_world',
    'cantopop': 'genre_world',
    'chicago-house': 'genre_electronic',
    'classical': 'genre_classical',
    'club': 'genre_electronic',
    'country': 'genre_rock',
    'dance': 'genre_pop',
    'dancehall': 'genre_reggae',
    'death-metal': 'genre_metal',
    'deep-house': 'genre_electronic',
    'detroit-techno': 'genre_electronic',
    'disco': 'genre_pop',
    'drum-and-bass': 'genre_electronic',
    'dub': 'genre_reggae',
    'dubstep': 'genre_electronic',
    'edm': 'genre_electronic',
    'electro': 'genre_electronic',
    'electronic': 'genre_electronic',
    'emo': 'genre_rock',
    'folk': 'genre_world',
    'forro': 'genre_latin',
    'french': 'genre_world',
    'funk': 'genre_jazz-soul',
    'garage': 'genre_electronic',
    'german': 'genre_world',
    'goth': 'genre_rock',
    'grindcore': 'genre_metal',
    'grunge': 'genre_rock',
    'hard-rock': 'genre_rock',
    'hardstyle': 'genre_electronic',
    'heavy-metal': 'genre_metal',
    'hip-hop': 'genre_hip-hop',
    'house': 'genre_electronic',
    'idm': 'genre_electronic',
    'indian': 'genre_world',
    'indie-pop': 'genre_pop',
    'indie': 'genre_rock',
    'industrial': 'genre_rock',
    'iranian': 'genre_world',
    'j-pop': 'genre_pop',
    'j-rock': 'genre_rock',
    'jazz': 'genre_jazz-soul',
    'k-pop': 'genre_pop',
    'latin': 'genre_latin',
    'latino': 'genre_latin',
    'malay': 'genre_world',
    'mandopop': 'genre_world',
    'metal': 'genre_metal',
    'metalcore': 'genre_metal',
    'minimal-techno': 'genre_electronic',
    'mpb': 'genre_latin',
    'opera': 'genre_classical',
    'pagode': 'genre_latin',
    'piano': 'genre_classical',
    'pop-film': 'genre_pop',
    'pop': 'genre_pop',
    'progressive-house': 'genre_electronic',
    'psych-rock': 'genre_rock',
    'punk-rock': 'genre_rock',
    'punk': 'genre_rock',
    'r-n-b': 'genre_jazz-soul',
    'reggae': 'genre_reggae',
    'reggaeton': 'genre_latin',
    'rock-n-roll': 'genre_rock',
    'rock': 'genre_rock',
    'rockabilly': 'genre_rock',
    'salsa': 'genre_latin',
    'samba': 'genre_latin',
    'sertanejo': 'genre_latin',
    'soul': 'genre_jazz-soul',
    'spanish': 'genre_world',
    'swedish': 'genre_world',
    'synth-pop': 'genre_pop',
    'techno': 'genre_electronic',
    'trance': 'genre_electronic',
    'trip-hop': 'genre_electronic',
    'turkish': 'genre_world',
    'world-music': 'genre_world',
}

def get_recommendations(db: Session, track_ids: list[str], n_neighbors: int = 5):
    if not ml_loader.model:
        return []

    input_songs = db.query(Song).filter(Song.track_id.in_(track_ids)).all()
    if not input_songs:
        print("Error: No songs found for the provided track IDs.")
        return []

    # Get genres of input songs to prioritize candidates
    input_genres = [s.track_genre for s in input_songs]
    input_categories = {GENRE_MAP.get(g, 'genre_inne') for g in input_genres}

    # Fetch candidate songs (filtered by categories for efficiency)
    # Mapping back categories to database genres
    relevant_db_genres = [g for g, cat in GENRE_MAP.items() if cat in input_categories]
    
    candidates_query = db.query(Song).filter(Song.track_genre.in_(relevant_db_genres))
    candidates = candidates_query.all()

    if not candidates:
        # Fallback to all songs if no genre match (shouldn't happen with broad categories)
        candidates = db.query(Song).limit(5000).all()

    feature_cols = [
        'danceability', 'energy', 'loudness', 'speechiness', 'acousticness', 
        'instrumentalness', 'liveness', 'valence', 'tempo'
    ]

    # Prepare data for prediction
    feature_names = feature_cols + GENRE_CATEGORIES
    data = []
    for s in candidates:
        features = [float(getattr(s, col)) for col in feature_cols]
        # Normalization
        features[2] = (features[2] + 50) / 55
        features[8] = features[8] / 250
        
        # One-hot genre
        genre_cat = GENRE_MAP.get(s.track_genre, 'genre_inne')
        genre_vec = [1 if cat == genre_cat else 0 for cat in GENRE_CATEGORIES]
        
        data.append(features + genre_vec)

    X = pd.DataFrame(data, columns=feature_names)
    # GBR prediction scores
    scores = ml_loader.model.predict(X)

    # Sort candidates by score descending
    sorted_indices = np.argsort(scores)[::-1]
    
    recommended_songs = []
    seen_track_ids = set(track_ids)
    
    for idx in sorted_indices:
        song = candidates[idx]
        if song.track_id not in seen_track_ids:
            recommended_songs.append(song)
            seen_track_ids.add(song.track_id)
        if len(recommended_songs) >= n_neighbors:
            break

    print(f"Sukcess: {len(recommended_songs)} recommendations found using GBR model.")
    return recommended_songs

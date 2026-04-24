from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from ..database.db_init import get_db
from ..services import predict_service
from ..schemas.songs_schema import SongResponse
from ..schemas.predict_schema import RecommendationRequest

router = APIRouter(prefix="/songs", tags=["songs"])

@router.post("/recommend", response_model=List[SongResponse])
def recommend_songs(request: RecommendationRequest, db: Session = Depends(get_db)):
    recommendations = predict_service.get_recommendations(db, request.track_ids)
    if not recommendations:
        return []
    return recommendations

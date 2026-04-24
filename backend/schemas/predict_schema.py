from pydantic import BaseModel
from typing import List

class RecommendationRequest(BaseModel):
    track_ids: List[str]

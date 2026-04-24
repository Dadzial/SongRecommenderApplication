from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database.db_init import engine, Base
from .routes import songs_route , predict_route

Base.metadata.create_all(bind=engine)

app = FastAPI(title="SongRecommender API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(songs_route.router)
app.include_router(predict_route.router)

@app.get("/")
def read_root():
    return {"message": "SongRecommender API is running"}

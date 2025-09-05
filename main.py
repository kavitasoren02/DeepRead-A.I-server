from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from routes import auth
from routes import file
from routes import chat
from routes import audio

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(" MongoDB connected and startup logic ran")
    yield
    print(" Server shutting down...")

app = FastAPI(lifespan=lifespan)

origins =[
    "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])

app.include_router(file.router, prefix='/api', tags=["UploadFile"])

app.include_router(chat.router, prefix='/api', tags=["ChatSummary"])

app.include_router(audio.router, prefix='/api', tags=["Audio"])

@app.get("/")
def read_root():
    return {"message": " FastAPI with MongoDB is running"}


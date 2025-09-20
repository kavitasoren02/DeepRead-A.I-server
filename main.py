from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from routes import auth
from routes import file
from routes import chat
from routes import audio
from routes import contact
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(" MongoDB connected and startup logic ran")
    yield
    print(" Server shutting down...")

app = FastAPI(lifespan=lifespan)

origins =[
    "http://localhost:5173",
    "http://192.168.1.2:5173"
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

app.include_router(contact.router, prefix='/api', tags=["Contact"])

# Expose audio folder as static files
app.mount("/api/audio_files", StaticFiles(directory="audio"), name="audio_files")

@app.get("/")
def read_root():
    return {"message": " FastAPI with MongoDB is running"}


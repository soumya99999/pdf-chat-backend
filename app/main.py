from fastapi import FastAPI
from app.database import init_db
from app.routes import upload, qa
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fullstack Internship Assignment API")

# CORS setup
origins = [
    "http://localhost:5173", "https://pdf-chat-frontend-nu.vercel.app" # React frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows requests from React frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize database tables
init_db()

# Include routers
app.include_router(upload.router, prefix="/api", tags=["uploads"])
app.include_router(qa.router, prefix="/api", tags=["questions"])

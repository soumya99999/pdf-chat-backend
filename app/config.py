import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

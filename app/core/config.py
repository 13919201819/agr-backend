import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASS = os.getenv("SMTP_PASS")
    HOST_EMAIL = os.getenv("HOST_EMAIL")

settings = Settings()
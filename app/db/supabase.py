from supabase import create_client
from app.core.config import settings

print("SUPABASE_URL:", settings.SUPABASE_URL)
print("SUPABASE_KEY:", settings.SUPABASE_KEY)

supabase = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)
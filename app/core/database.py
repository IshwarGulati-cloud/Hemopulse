from functools import lru_cache

from supabase import create_client, Client
from app.core.config import settings


@lru_cache
def get_supabase_client() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise ValueError("Supabase environment variables are missing.")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

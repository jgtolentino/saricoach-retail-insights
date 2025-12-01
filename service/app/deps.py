from .config import settings
from .backend.csv_backend import CSVBackend
from .backend.supabase_backend import SupabaseBackend

def get_backend():
    if settings.data_backend == "supabase":
        if not settings.database_url:
            raise ValueError("SARICOACH_DATA_BACKEND is 'supabase' but SARICOACH_DATABASE_URL is missing.")
        return SupabaseBackend(settings.database_url)
    
    # Default to CSV/Mock
    return CSVBackend(base_path="data/processed")

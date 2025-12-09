# supabase_client.py

# ===========================================
# CONFIGURACIÓN SUPABASE PARA USAR REST API
# ===========================================

SUPABASE_URL = "https://urtmzqvthdhberemipcd.supabase.co"

# *** USAR SIEMPRE LA ANON KEY PARA EL BACKEND REST ***
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVydG16cXZ0aGRoYmVyZW1pcGNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjUxODk0ODIsImV4cCI6MjA4MDc2NTQ4Mn0.z1UIQCu6FiZNSmOnXBIpDRQnGyOlExYbIepBBzuJQqk"

SUPABASE_HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

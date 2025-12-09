import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_super_secreta_para_tfg")
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:macg410BB.@db.urtmzqvthdhberemipcd.supabase.co:5432/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "clave_para_jwt")

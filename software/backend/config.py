"""Configurações do backend Flask."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///tcc_grupo6.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    API_TOKEN = os.getenv("API_TOKEN", "troque_este_token")
    TEMP_MIN = float(os.getenv("TEMP_MIN", 15.0))
    TEMP_MAX = float(os.getenv("TEMP_MAX", 30.0))
    UMIDADE_MIN = float(os.getenv("UMIDADE_MIN", 40.0))
    UMIDADE_MAX = float(os.getenv("UMIDADE_MAX", 70.0))

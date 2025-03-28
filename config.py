# app/config.py
class Settings:
    cors_origins = ["http://localhost:3000", "http://localhost:3001"]
    host_url = "127.0.0.1:8000" #Example configuration, move to env later

settings = Settings()

from fastapi import FastAPI
from src.endpoints import register_endpoints

# Создаём приложение FastAPI
app = FastAPI()

# Регистрируем эндпойнты
register_endpoints(app)
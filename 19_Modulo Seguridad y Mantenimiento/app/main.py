from fastapi import FastAPI

from app.config import settings

app = FastAPI(title="API Modulo Seguridad y mantenimiento")


@app.get("/")
def health_check() -> dict:
    return {
        "status": "ok",
        # Pydantic lo oculta como '**********'
        "api_key_cifrada": str(settings.api_key),
    }

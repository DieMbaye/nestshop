from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.database import engine
from app.routers import products  

app = FastAPI(title="NestShop API", version="0.1.0")

app.include_router(products.router)  


@app.get("/health", tags=["Santé"])
def health():
    try:
        with engine.connect() as connexion:
            connexion.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "error", "database": "indisponible"},
        )
    return {"status": "ok", "database": "ok"}
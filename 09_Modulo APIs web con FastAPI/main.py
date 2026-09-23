from typing import Annotated

from auth import Token, crear_token
from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from routers import orders

app = FastAPI(title="API con FastAPI", version="1.0")

# Config. del middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)


# Conexión de routers y endpoints

# Conectamos el router
app.include_router(orders.router, prefix="/api/v1")


@app.post("/login", response_model=Token, tags=["Autenticación"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.username != "admin" or form_data.password != "secreto":
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    token = crear_token(username=form_data.username)
    return {"access_token": token, "token_type": "bearer"}

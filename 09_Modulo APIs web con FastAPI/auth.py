from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

SECRET_KEY = "secret"
ALGORITHM = "HS256"


class Token(BaseModel):
    access_token: str
    token_type: str


# Configura Swagger para que muestre el botón "Authorize" y apunte a /login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def crear_token(username: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=30)
    datos = {"sub": username, "exp": expira}
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except Exception:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado"
        )

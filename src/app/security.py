import secrets
from fastapi import Security
from fastapi import HTTPException, status
from fastapi.security import APIKeyHeader
from app.config import API_SECRET_KEY

API_KEY_HEADER_NAME = "X-API-KEY"

api_key_scheme = APIKeyHeader(name=API_KEY_HEADER_NAME, auto_error=False)

def validate_api_key(api_key: str = Security(api_key_scheme)):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=f"Acesso negado: Chave de API ('{API_KEY_HEADER_NAME}') ausente"
        )

    api_key_matches = secrets.compare_digest(api_key, API_SECRET_KEY)

    if not api_key_matches:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Acesso negado: Chave de API ('{API_KEY_HEADER_NAME}') inválida"
        )

    return api_key

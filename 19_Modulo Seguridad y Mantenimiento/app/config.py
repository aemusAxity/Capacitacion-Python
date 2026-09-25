from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # 'SecretStr' evita que la contraseña se imprima en los logs por accidente
    db_password: SecretStr
    api_key: SecretStr
    debug_mode: bool = False  # Tiene valor por defecto, no es obligatoria en el .env

    # Configuración estricta: lee del .env y prohíbe variables extrañas
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Instanciamos la configuración. Si faltan secretos,
# la app no arrancará.
settings = Settings()

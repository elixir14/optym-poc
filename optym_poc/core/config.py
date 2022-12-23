
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DATABASE_TYPE: str = "postgresql"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_DB: str
    MYSQL_PORT: int = 5432

    DATABASE_URI: Optional[str] = None

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if values.get("DATABASE_TYPE") == "postgresql":
            if isinstance(v, str):
                return v
            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_HOST"),
                path=f"/{values.get('POSTGRES_DB') or ''}",
            )
        return "mysql+pymysql://{0}:{1}@{2}/{3}".format(
            values.get("MYSQL_USER"),
            quote(values.get("MYSQL_PASSWORD")),
            values.get("MYSQL_HOST"),
            values.get('MYSQL_DB')
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

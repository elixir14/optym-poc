
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote

from pydantic import AnyHttpUrl, BaseSettings, PostgresDsn, validator, Field


class Settings(BaseSettings):
    PROJECT_NAME: str
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    DATABASE_TYPE: str = "postgresql"

    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_HOST: str
    DATABASE_DB: str
    DATABASE_PORT: int = 5432

    DATABASE_URI: Optional[str] = None

    OPENAPI_CLIENT_ID: str = Field(default='', env='OPENAPI_CLIENT_ID')
    APP_CLIENT_ID: str = Field(default='', env='APP_CLIENT_ID')
    TENANT_ID: str = Field(default='', env='TENANT_ID')

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
            # if isinstance(v, str):
            #     return v
            print("Print: ", values.get("DATABASE_PASSWORD"))
            return PostgresDsn.build(
                scheme="postgresql",
                user=values.get("DATABASE_USER"),
                password=quote(values.get("DATABASE_PASSWORD")),
                host=values.get("DATABASE_HOST"),
                path=f"/{values.get('DATABASE_DB') or ''}",
                port=str(values.get("DATABASE_PORT"))
            )
        return "mysql+pymysql://{0}:{1}@{2}/{3}".format(
            values.get("DATABASE_USER"),
            quote(values.get("DATABASE_PASSWORD")),
            values.get("DATABASE_HOST"),
            values.get('DATABASE_DB')
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

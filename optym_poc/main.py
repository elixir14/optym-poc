import logging
import time
import uuid
from contextvars import ContextVar

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Match

from apps.loads.api.v1 import load_router
from optym_poc.core.config import settings
from optym_poc.core.logs import setup_logging
from optym_poc.core.services.azure import azure_scheme

logger = logging.getLogger(__name__)


def get_application():
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url="/",
        swagger_ui_oauth2_redirect_url='/oauth2-redirect',
        swagger_ui_init_oauth={
            'usePkceWithAuthorizationCodeGrant': True,
            'clientId': settings.OPENAPI_CLIENT_ID,
        },
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()
request_id_contextvar = ContextVar("request_id", default=None)


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    status_code = exc.status_code if hasattr(exc, 'status_code') else 500
    logger.error(
        "OptymHTTPException raised. Request: %s, user: %s. Error: %s, Code: -1, Status: %s",
        request.url.path, request.scope.get('auth', None), exc.__dict__, status_code
    )
    return JSONResponse(
        {"message": exc.__dict__.get('message', "Something went wrong"), "error_code": -1},
        status_code=status_code,
    )


@app.middleware("http")
async def request_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    request_url = str(request.url)
    request_id_contextvar.set(request_id)
    request_method = request.method
    start_time = time.time()
    logger.info(f"Request started, Method:{request_method}, URL: {request_url}")
    routes = request.app.router.routes
    logger.debug("Request Params:")
    for route in routes:
        match, scope = route.matches(request)
        if match == Match.FULL:
            for name, value in scope["path_params"].items():
                logger.debug(f"\t{name}: {value}")
    logger.debug("Request Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")

    try:
        return await call_next(request)
    except Exception as ex:
        logger.error(f"Request failed: {ex}")
        raise
    finally:
        logger.info("Time took to process the request and return response is {} sec".format(
            time.time() - start_time
        ))
        logger.info(f"Request Ended, Method:{request_method}, URL: {request_url}")


@app.on_event("startup")
async def startup_event():
    setup_logging()


@app.on_event('startup')
async def load_config() -> None:
    """
    Load OpenID config on startup.
    """
    await azure_scheme.openid_config.load_config()


app.include_router(load_router)

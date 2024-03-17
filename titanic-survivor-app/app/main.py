import logging.config

from typing import Any
from fastapi import APIRouter, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.api import api_router
from app.config import get_settings
from app.log_config import app_config


# Initialize the app config
logging.config.dictConfig(app_config.log_config)
logger = app_config.get_logger()

# Initialize the app settings
settings = get_settings()

# Initialize the app and router
logger.info(f"Initializing the {settings.PROJECT_NAME}...")
app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")
root_router = APIRouter()


@app.get("/")
def index(request: Request) -> Any:
    """Index HTML response."""
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Check the docs: <a href='/docs'>here</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return HTMLResponse(content=body)


logger.debug("Initializing api_router...")
app.include_router(api_router, prefix=settings.API_V1_STR)
logger.debug("Initializing root_router...")
app.include_router(root_router)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


if __name__ == "__main__":
    # Use this for debugging purposes only
    logger.warning("Running in development mode. Do not run like this in production.")
    import uvicorn

    uvicorn.run(app, host="localhost", port=8001)

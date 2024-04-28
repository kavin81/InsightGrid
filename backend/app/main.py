from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from app.api import api_router
from app.core import lifespan, settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    openapi_url=settings.OPENAPI_URL,
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    lifespan=lifespan,
)


@app.get("/", tags=["healthcheck"])
async def root() -> RedirectResponse:
    return RedirectResponse(
        url=settings.DOCS_URL,
        status_code=301,
    )


app.include_router(api_router, prefix=settings.API_VER)

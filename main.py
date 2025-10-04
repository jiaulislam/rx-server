import sentry_sdk
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.route.v1 import routeros_router  # noqa
from app.settings import Settings
from app.settings.middleware import ProcessTimeMiddleware

from devtools import debug  # ignore: isort:skip


load_dotenv()  # Load environment variables from .env file

settings = Settings()


sentry_sdk.init(
    dsn=settings.sentry_dsn,
    send_default_pii=True,
)

routes = [routeros_router]

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(ProcessTimeMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_cors_origins,
    allow_credentials=settings.allow_credentials,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.allowed_hosts,
)

for route in routes:
    app.include_router(route)


debug(settings)


@app.get("/")
async def read_root():
    return {"message": f"Welcome to the {settings.app_name}!"}

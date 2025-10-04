import sentry_sdk
from dotenv import load_dotenv
from fastapi import FastAPI

from app.route.v1 import routeros_router  # noqa
from app.settings import Settings

load_dotenv()  # Load environment variables from .env file

settings = Settings()  # pyright: ignore


sentry_sdk.init(
    dsn="",
    send_default_pii=True,
)

routes = [routeros_router]

app = FastAPI(title=settings.app_name, debug=settings.debug)

for route in routes:
    app.include_router(route)


@app.get("/")
async def read_root():
    return {"message": f"Welcome to the {settings.app_name}!"}

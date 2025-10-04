import sentry_sdk
from app.lib.mikrotik_routeros.application.use_cases import GetSystemResourceUseCase
from app.lib.mikrotik_routeros.infrastructure.mikrotik import (
    MikroTikSystemResourceRepository,
)
from app.lib.mikrotik_routeros.infrastructure.mikrotik.types import (
    MikrotikConnecitonConfig,
)
from dotenv import load_dotenv
from fastapi import FastAPI

from app.settings import Settings

load_dotenv()  # Load environment variables from .env file

settings = Settings()  # pyright: ignore


sentry_sdk.init(
    dsn="https://ff9e5a10bf4538ee255397538fc9d198@o1396988.ingest.us.sentry.io/4508085957623808",
    # Add data like request headers and IP for users, if applicable;
    # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
    send_default_pii=True,
)

app = FastAPI(title=settings.app_name, debug=settings.debug)


@app.get("/")
async def read_root():
    return {"message": f"Welcome to the {settings.app_name}!"}


@app.get("/mikrotik/system-resource")
async def get_mikrotik_resource():
    mikrotik_connection_config = MikrotikConnecitonConfig(
        host=settings.routeros.host,
        username=settings.routeros.username,
        password=settings.routeros.password,
        port=settings.routeros.port,
    )
    use_case = GetSystemResourceUseCase(
        system_resource_repo=MikroTikSystemResourceRepository(
            mikrotik_connection_config
        ),
    )
    response = await use_case.execute(mikrotik_connection_config)
    return response

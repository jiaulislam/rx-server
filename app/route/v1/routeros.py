from fastapi import APIRouter

from app.lib.routeros.application.use_cases import GetSystemResourceUseCase
from app.lib.routeros.infrastructure.mikrotik import (
    MikroTikSystemResourceRepository,
)
from app.lib.routeros.infrastructure.mikrotik.types import (
    MikrotikConnectionConfig,
)
from app.settings import Settings

settings = Settings()  # pyright: ignore

router = APIRouter(prefix="/v1/routeros", tags=["routeros"])


@router.get("/system-resource")
async def get_mikrotik_resource():
    mikrotik_connection_config = MikrotikConnectionConfig(
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

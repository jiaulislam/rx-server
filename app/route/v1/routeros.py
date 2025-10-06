from fastapi import APIRouter
from loguru import logger

from app.core import Settings
from app.core.structure import BaseResponse
from app.lib.routeros.application.use_cases import GetSystemResourceUseCase
from app.lib.routeros.domain.entities import SystemResource
from app.lib.routeros.infrastructure.mikrotik.system_resource_repository import (
    MikroTikSystemResourceRepository,
)
from app.lib.routeros.infrastructure.mikrotik.types import (
    MikrotikConnectionConfig,
)

settings = Settings()  # pyright: ignore

router = APIRouter(prefix="/v1/routeros", tags=["routeros"])


@router.get("/system-resource", response_model=BaseResponse[SystemResource])
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
    logger.info(
        "Fetching system resource from MikroTik router at {}",
        mikrotik_connection_config.host,
    )
    response = await use_case.execute(mikrotik_connection_config)
    return response

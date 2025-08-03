from .default import default_router
from .markets import markets_router
from .scripts import scripts_router


routers = [
    scripts_router,
    markets_router,
    default_router,
]

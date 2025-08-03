from .default import default_router
from .markets import markets_router


routers = [
    markets_router,
    default_router,
]

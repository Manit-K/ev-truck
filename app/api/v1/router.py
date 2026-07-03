from fastapi import APIRouter

from app.api.v1.endpoints.health import router as health_router
from app.api.v1.endpoints.integrations import router as integrations_router
from app.api.v1.endpoints.optimization import router as optimization_router
from app.api.v1.endpoints.trips import router as trips_router
from app.api.v1.endpoints.vehicles import router as vehicles_router

api_router = APIRouter()

api_router.include_router(
    health_router,
    tags=["Health"],
)
api_router.include_router(vehicles_router, tags=["Vehicles"])
api_router.include_router(trips_router, tags=["Trips"])
api_router.include_router(integrations_router, tags=["Integrations"])
api_router.include_router(optimization_router, tags=["Optimization"])

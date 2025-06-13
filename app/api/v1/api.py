from fastapi import APIRouter
from app.api.v1.endpoints import devices
from app.api.v1.endpoints import vulnerability

api_router = APIRouter()

api_router.include_router(devices.router)
api_router.include_router(
    vulnerability.router, prefix="/vulnerabilities", tags=["vulnerabilities"]
)

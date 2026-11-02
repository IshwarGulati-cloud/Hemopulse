from fastapi import APIRouter
from app.api.v1.endpoints import predict, facilities

api_router = APIRouter()
api_router.include_router(predict.router, prefix="/predict", tags=["Screening & Prediction"])
api_router.include_router(facilities.router, prefix="/facilities", tags=["Rural Healthcare Catalog"])
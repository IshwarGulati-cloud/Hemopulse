from fastapi import APIRouter, HTTPException, Query, status
from typing import List
from app.schemas.facility import HealthcareFacilitySchema
from app.services.hospital_service import hospital_service

router = APIRouter()

@router.get("/", response_model=List[HealthcareFacilitySchema], status_code=status.HTTP_200_OK)
async def get_healthcare_facilities(
    level: int = Query(None, ge=1, le=3),
    latitude: float = Query(None, ge=-90, le=90),
    longitude: float = Query(None, ge=-180, le=180),
    radius_km: float = Query(None, gt=0, le=500),
):
    if (latitude is None) != (longitude is None):
        raise HTTPException(status_code=422, detail="Latitude and longitude must be provided together.")
    if radius_km is not None and latitude is None:
        raise HTTPException(status_code=422, detail="A radius requires latitude and longitude.")
    try:
        if latitude is not None:
            facilities = hospital_service.get_nearby_facilities(latitude, longitude, level, radius_km)
        elif level is not None:
            facilities = hospital_service.get_facilities_by_level(level)
        else:
            facilities = hospital_service.get_all_facilities()
        return facilities
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch facility catalog.")

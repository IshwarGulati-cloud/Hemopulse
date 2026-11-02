from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class HealthcareFacilitySchema(BaseModel):
    id: UUID
    name: str
    facility_type: Optional[str] = None
    referral_level: Optional[int] = Field(None, ge=1, le=3)
    address: str
    phone: Optional[str] = None
    latitude: float
    longitude: float
    google_maps_url: Optional[str] = None
    distance_km: Optional[float] = None

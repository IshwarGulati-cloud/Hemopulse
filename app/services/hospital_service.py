from math import atan2, cos, radians, sin, sqrt

from app.core.database import get_supabase_client

class HospitalService:
    @staticmethod
    def get_all_facilities():
        response = get_supabase_client().table("healthcare_facilities").select("*").execute()
        return response.data

    @staticmethod
    def get_facilities_by_level(level: int):
        response = get_supabase_client().table("healthcare_facilities").select("*").eq("referral_level", level).execute()
        return response.data

    @staticmethod
    def get_nearby_facilities(
        latitude: float,
        longitude: float,
        level: int = None,
        radius_km: float = None,
    ):
        facilities = (
            HospitalService.get_facilities_by_level(level)
            if level is not None
            else HospitalService.get_all_facilities()
        )
        for facility in facilities:
            lat1, lon1, lat2, lon2 = map(
                radians,
                [latitude, longitude, facility["latitude"], facility["longitude"]],
            )
            delta_lat, delta_lon = lat2 - lat1, lon2 - lon1
            a = min(1, sin(delta_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(delta_lon / 2) ** 2)
            facility["distance_km"] = round(6371 * 2 * atan2(sqrt(a), sqrt(1 - a)), 2)
        facilities = [
            facility
            for facility in facilities
            if radius_km is None or facility["distance_km"] <= radius_km
        ]
        return sorted(facilities, key=lambda facility: facility["distance_km"])

hospital_service = HospitalService()

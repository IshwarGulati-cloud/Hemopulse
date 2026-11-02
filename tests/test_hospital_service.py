import unittest
from unittest.mock import patch

from app.services.hospital_service import HospitalService


class NearbyFacilityTests(unittest.TestCase):
    @patch("app.services.hospital_service.get_supabase_client")
    def test_reads_facilities_table(self, get_client):
        client = get_client.return_value
        client.table.return_value.select.return_value.execute.return_value.data = []

        result = HospitalService.get_all_facilities()

        self.assertEqual(result, [])
        client.table.assert_called_once_with("healthcare_facilities")

    @patch("app.services.hospital_service.get_supabase_client")
    def test_filters_facilities_by_referral_level(self, get_client):
        client = get_client.return_value
        client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

        HospitalService.get_facilities_by_level(2)

        client.table.return_value.select.return_value.eq.assert_called_once_with("referral_level", 2)

    def test_sorts_by_distance_and_adds_distance(self):
        facilities = [
            {"name": "Far", "latitude": 1.0, "longitude": 0.0},
            {"name": "Near", "latitude": 0.1, "longitude": 0.0},
        ]
        with patch.object(HospitalService, "get_all_facilities", return_value=facilities):
            result = HospitalService.get_nearby_facilities(0.0, 0.0)

        self.assertEqual([item["name"] for item in result], ["Near", "Far"])
        self.assertGreater(result[0]["distance_km"], 0)

    def test_applies_optional_radius(self):
        facilities = [
            {"name": "Far", "latitude": 1.0, "longitude": 0.0},
            {"name": "Near", "latitude": 0.1, "longitude": 0.0},
        ]
        with patch.object(HospitalService, "get_all_facilities", return_value=facilities):
            result = HospitalService.get_nearby_facilities(0.0, 0.0, radius_km=20)

        self.assertEqual([item["name"] for item in result], ["Near"])

import unittest

from fastapi import FastAPI

from app.api.v1.endpoints.facilities import router


class FacilityEndpointTests(unittest.TestCase):
    def test_rejects_invalid_referral_level(self):
        app = FastAPI()
        app.include_router(router)
        level = app.openapi()["paths"]["/"]["get"]["parameters"][0]

        self.assertEqual(level["schema"]["minimum"], 1)
        self.assertEqual(level["schema"]["maximum"], 3)


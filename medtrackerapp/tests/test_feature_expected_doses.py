from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from medtrackerapp.models import Medication


class ExpectedDosesEndpointTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.med = Medication.objects.create(
            name="TestMed", dosage_mg=100, prescribed_per_day=2
        )

    def test_expected_doses_success(self):
        url = f"/api/medications/{self.med.id}/expected-doses/?days=5"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data["medication_id"], self.med.id)
        self.assertEqual(data["days"], 5)
        self.assertEqual(data["expected_doses"], 10)

    def test_expected_doses_missing_days(self):
        url = f"/api/medications/{self.med.id}/expected-doses/"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expected_doses_invalid_days_nonint(self):
        url = f"/api/medications/{self.med.id}/expected-doses/?days=abc"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expected_doses_invalid_days_negative(self):
        url = f"/api/medications/{self.med.id}/expected-doses/?days=-1"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_expected_doses_model_value_error(self):
        # Force the model's expected_doses to raise (simulate bad prescription)
        self.med.prescribed_per_day = 0
        self.med.save()
        url = f"/api/medications/{self.med.id}/expected-doses/?days=5"
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from medtrackerapp.models import Medication

class NotesFeatureTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.med = Medication.objects.create(name="NoteMed", dosage_mg=10, prescribed_per_day=1)

    def test_create_note(self):
        payload = {"medication": self.med.id, "text": "Doctor says rest"}
        resp = self.client.post("/api/notes/", payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        self.assertIn("id", data)
        self.assertEqual(data["medication"], self.med.id)
        self.assertEqual(data["text"], "Doctor says rest")

    def test_list_notes_empty(self):
        resp = self.client.get("/api/notes/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.json()), 0)

    def test_retrieve_note_not_found(self):
        resp = self.client.get("/api/notes/999/")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_note(self):
        create = self.client.post("/api/notes/", {"medication": self.med.id, "text":"x"}, format="json")
        nid = create.json()["id"]
        resp = self.client.delete(f"/api/notes/{nid}/")
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

HEADER = b"Equipment Name,Type,Flowrate,Pressure,Temperature\n"
GOOD = HEADER + b"Pump-1,Pump,120,5.2,110\nValve-1,Valve,60,4.1,105\n"
MEDIA = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA)
class UploadAPITests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA, ignore_errors=True)

    def setUp(self):
        User.objects.create_user("engineer", password="secret-pass")
        self.client = APIClient()
        response = self.client.post(
            "/api/login/",
            {"username": "engineer", "password": "secret-pass"},
            format="json",
        )
        self.client.credentials(HTTP_AUTHORIZATION="Token " + response.json()["token"])

    def upload(self, body, name="data.csv"):
        file = SimpleUploadedFile(name, body, content_type="text/csv")
        return self.client.post("/api/upload/", {"file": file}, format="multipart")

    def test_upload_summarises_the_csv(self):
        response = self.upload(GOOD)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["summary"],
            {
                "total_equipment": 2,
                "average_flowrate": 90.0,
                "average_pressure": 4.65,
                "average_temperature": 107.5,
                "equipment_type_distribution": {"Pump": 1, "Valve": 1},
            },
        )

    def test_blank_cells_are_skipped_in_averages(self):
        response = self.upload(HEADER + b"P1,Pump,100,5,110\nP2,Pump,,7,90\n")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["summary"]["average_flowrate"], 100.0)
        self.assertEqual(response.json()["summary"]["average_pressure"], 6.0)

    def test_rejected_files_get_a_clear_message(self):
        cases = {
            b"": "Invalid CSV file",
            b"a,b\n1,2\n": "CSV missing required columns",
            HEADER: "CSV has no data rows",
            HEADER + b"P1,Pump,fast,5,110\n": "Flowrate must be a number; found 'fast' in row 2",
            HEADER + b"P1,Pump,100,,110\n": "Pressure has no values",
        }
        for body, message in cases.items():
            with self.subTest(message=message):
                response = self.upload(body)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.json()["error"], message)

    def test_only_the_last_five_datasets_are_kept(self):
        for index in range(7):
            self.upload(GOOD, name=f"data{index}.csv")
        self.assertEqual(len(self.client.get("/api/datasets/").json()), 5)

    def test_pdf_report_downloads(self):
        dataset_id = self.upload(GOOD).json()["id"]
        response = self.client.get(f"/api/datasets/{dataset_id}/pdf/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
        self.assertEqual(self.client.get("/api/datasets/999/pdf/").status_code, 404)

    def test_endpoints_need_a_token(self):
        anonymous = APIClient()
        self.assertEqual(anonymous.post("/api/upload/").status_code, 401)
        self.assertEqual(anonymous.get("/api/datasets/").status_code, 401)

    def test_wrong_password_is_refused(self):
        response = APIClient().post(
            "/api/login/", {"username": "engineer", "password": "nope"}, format="json"
        )
        self.assertEqual(response.status_code, 400)

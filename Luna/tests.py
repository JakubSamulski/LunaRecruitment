from datetime import datetime, timedelta

from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import HydroponicSystem, Reading

User = get_user_model()


class HydroponicSystemTests(APITestCase):
    fixtures = ["Luna/fixtures/test.json"]

    # write some tests here
    def setUp(self):
        self.user = User.objects.get(username="newuser")
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.admin_system_pk = 2  # Admin's system (pk=2)
        self.user_system_pk = 3  # User's system (pk=3)
        self.user_system = HydroponicSystem.objects.get(pk=self.user_system_pk)

    def test_create_hydroponic_system(self):
        url = reverse("hydroponic system-list")
        data = {
            "name": "Test System",
            "description": "Test Description",
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(HydroponicSystem.objects.count(), 4)
        self.assertEqual(
            HydroponicSystem.objects.get(id=response.data["id"]).name, "Test System"
        )
        self.assertEqual(
            HydroponicSystem.objects.get(id=response.data["id"]).description,
            "Test Description",
        )

    def test_list_systems(self):
        response = self.client.get(reverse("hydroponic system-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        system_ids = [sys["id"] for sys in response.data["results"]]
        self.assertListEqual(system_ids, [3, 4])

    def test_retrieve_own_system(self):
        response = self.client.get(
            reverse("hydroponic system-detail", args=[self.user_system_pk])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.user_system_pk)

    def test_retrieve_others_system(self):
        response = self.client.get(
            reverse("hydroponic system-detail", args=[self.admin_system_pk])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_system(self):
        url = reverse("hydroponic system-detail", args=[self.user_system_pk])
        data = {
            "name": "Updated System",
            "description": "Updated Description",
        }
        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            HydroponicSystem.objects.get(id=self.user_system_pk).name, "Updated System"
        )
        self.assertEqual(
            HydroponicSystem.objects.get(id=self.user_system_pk).description,
            "Updated Description",
        )

    def test_delete_system(self):
        response = self.client.delete(
            reverse("hydroponic system-detail", args=[self.user_system_pk])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            HydroponicSystem.objects.filter(id=self.user_system_pk).exists()
        )

    def test_system_detail_with_readings(self):
        for i in range(15):
            Reading.objects.create(
                hydroponic_system=self.user_system,
                temperature=20 + i,
                ph=6.0 + i / 10,
                tds=500 + i * 10,
                timestamp=make_aware(datetime.now() - timedelta(hours=15 - i)),
            )

        response = self.client.get(
            reverse("hydroponic system-detail", args=[self.user_system_pk])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["latest_readings"]), 10)
        self.assertEqual(
            response.data["latest_readings"][0]["temperature"], 34.0
        )  # Najnowszy
        self.assertEqual(
            response.data["latest_readings"][-1]["temperature"], 25.0
        )  # Najstarszy z 10


class ReadingTests(APITestCase):
    fixtures = ["Luna/fixtures/test.json"]

    def setUp(self):
        self.user = User.objects.get(username="newuser")
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.user_system_pk = 3  # User's system
        self.admin_reading_pk = 5  # Admin's reading (pk=5)

    def test_unauthenticated_access(self):
        self.client.credentials()
        response = self.client.get(reverse("reading-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_readings(self):
        response = self.client.get(reverse("reading-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)
        reading_ids = {r["id"] for r in response.data["results"]}
        self.assertSetEqual(reading_ids, {2, 3, 4})

    def test_retrieve_others_reading(self):
        response = self.client.get(
            reverse("reading-detail", args=[self.admin_reading_pk])
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_by_system(self):
        response = self.client.get(
            reverse("reading-list"), {"hydroponic_system": self.user_system_pk}
        )
        self.assertEqual(len(response.data["results"]), 2)
        reading_ids = {r["id"] for r in response.data["results"]}
        self.assertSetEqual(reading_ids, {2, 3})

    def test_filter_by_timestamp(self):
        response = self.client.get(
            reverse("reading-list"),
            {
                "timestamp_after": "2025-02-20T20:22:00Z",
                "timestamp_before": "2025-02-20T20:23:00Z",
            },
        )
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["id"], 4)

    def test_ordering(self):
        response = self.client.get(reverse("reading-list"))
        timestamps = [r["timestamp"] for r in response.data["results"]]
        self.assertEqual(timestamps, sorted(timestamps, reverse=True))

        response = self.client.get(reverse("reading-list"), {"ordering": "timestamp"})
        timestamps = [r["timestamp"] for r in response.data["results"]]
        self.assertEqual(timestamps, sorted(timestamps))

    def test_create_reading(self):
        data = {
            "hydroponic_system": self.user_system_pk,
            "temperature": 25.0,
            "ph": 6.5,
            "tds": 500.0,
            "timestamp": "2025-02-20T20:30:00Z",
        }
        response = self.client.post(reverse("reading-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Reading.objects.filter(id=response.data["id"]).exists())

    def test_create_reading_invalid_system(self):
        data = {
            "hydroponic_system": 2,  # Admin's system
            "temperature": 25.0,
            "ph": 6.5,
            "tds": 500.0,
            "timestamp": "2025-02-20T20:30:00Z",
        }
        response = self.client.post(reverse("reading-list"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("hydroponic_system", response.data)

    def test_delete_reading(self):
        response = self.client.delete(reverse("reading-detail", args=[2]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reading.objects.filter(id=2).exists())

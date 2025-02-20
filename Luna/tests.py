from django.urls.base import reverse
from rest_framework.test import APITestCase
from rest_framework import status


class HydroponicSystemTests(APITestCase):
    fixtures = ["Luna/fixtures/test.json"]

    # Authentication Tests
    def test_list_systems_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse("hydroponic system-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

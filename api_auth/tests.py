from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class TestUserRegistration(APITestCase):
    def setUp(self):
        self.url = reverse("register")
        self.valid_data = {
            "username": "testuser",
            "password": "testpass123",
            "email": "test@example.com",
        }

    def test_create_user_valid_data(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())
        self.assertNotIn("password", response.data)

    def test_create_user_missing_username(self):
        data = self.valid_data.copy()
        del data["username"]
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)

    def test_create_user_missing_password(self):
        data = self.valid_data.copy()
        del data["password"]
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_password_is_write_only(self):
        response = self.client.post(self.url, self.valid_data)
        self.assertNotIn("password", response.data)


class TestAuthToken(APITestCase):
    def setUp(self):
        self.url = reverse("token")
        self.user = User.objects.create_user(
            username="existinguser",
            password="validpass123",
            email="existing@example.com",
        )
        self.valid_credentials = {
            "username": "existinguser",
            "password": "validpass123",
        }

    def test_obtain_token_valid_credentials(self):
        response = self.client.post(self.url, self.valid_credentials)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        token = Token.objects.get(user=self.user)
        self.assertEqual(response.data["token"], token.key)

    def test_obtain_token_invalid_password(self):
        data = self.valid_credentials.copy()
        data["password"] = "wrongpass"
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_obtain_token_nonexistent_user(self):
        data = {"username": "nonexistent", "password": "anypass"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

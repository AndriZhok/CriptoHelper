from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from user.serializers import UserSerializer

User = get_user_model()


class UserManagerTests(APITestCase):
    def test_create_user_with_email_successful(self):
        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_successful(self):
        user = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )
        self.assertEqual(user.email, "admin@example.com")
        self.assertTrue(user.check_password("adminpass123"))
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None, password="testpass123")


class UserSerializerTests(APITestCase):
    def test_user_serializer_create(self):
        serializer = UserSerializer(
            data={"email": "test@example.com", "password": "testpass123"}
        )
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))

    def test_user_serializer_update(self):
        user = User.objects.create_user(
            email="test@example.com", password="oldpassword"
        )
        serializer = UserSerializer(
            instance=user, data={"password": "newpassword"}, partial=True
        )
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertTrue(updated_user.check_password("newpassword"))


class CreateUserViewTests(APITestCase):
    def test_create_user(self):
        url = reverse("user:create")
        payload = {"email": "testuser@example.com", "password": "testpass123"}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], payload["email"])
        self.assertNotIn("password", response.data)


class ManageUserViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpass123"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

    def test_retrieve_user_profile(self):
        url = reverse("user:manage")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_update_user_profile(self):
        url = reverse("user:manage")
        payload = {"password": "newpassword123"}
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload["password"]))

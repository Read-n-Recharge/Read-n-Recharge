from django.test import TestCase
from .models import User
from .serializer import RegisterSerializer, StudyPreferenceSerializer
from rest_framework import status
from django.contrib.auth import get_user_model


class RegisterTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            email="existing@example.com",
            first_name="Existing",
            last_name="User",
            password="ComplexPass123!",
        )

    def test_register_valid(self):
        data = {
            "email": "newuser@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "ComplexPass123!",
            "confirm_password": "ComplexPass123!",
        }
        response = self.client.post("/auth/register/", data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())

    def test_register_existing_email(self):
        data = {
            "email": "existing@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "password": "ComplexPass123!",
            "confirm_password": "ComplexPass123!",
        }
        response = self.client.post("/auth/register/", data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)


class RegisterDuplicateEmailTestCase(TestCase):

    def setUp(self):
        User.objects.create(
            first_name="Existing",
            last_name="User",
            email="Supinee@gmail.com",
            password="ExistingPass123",
        )

    def test_register_duplicate_email(self):
        data = {
            "first_name": "Putiphuk",
            "last_name": "Saisuwan",
            "email": "Supinee@gmail.com",
            "password": "Phutub2003",
            "confirm_password": "Phutub2003",
        }

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("email", serializer.errors)
        self.assertEqual(
            serializer.errors["email"][0],
            "user with this email already exists.",
        )


class RegisterPasswordMismatchTestCase(TestCase):

    def test_register_password_mismatch(self):
        data = {
            "first_name": "Uncharee",
            "last_name": "Suwantawiwat",
            "email": "Keepypie47@gmail.com",
            "password": "Keepypie11",
            "confirm_password": "Keepypie123",
        }

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("password", serializer.errors)
        self.assertEqual(
            serializer.errors["password"][0], "Password fields didn't match."
        )


class RegisterInvalidEmailFormatTestCase(TestCase):

    def test_register_invalid_email_format(self):
        data = {
            "first_name": "Uncharee",
            "last_name": "Suwantawiwat",
            "email": "Keepypiecom",
            "password": "CorrectPassword123",
            "confirm_password": "CorrectPassword123",
        }

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("email", serializer.errors)
        self.assertEqual(serializer.errors["email"][0], "Enter a valid email address.")


class RegisterInvalidPasswordLengthTestCase(TestCase):

    def test_register_password_too_short(self):
        data = {
            "first_name": "Uncharee",
            "last_name": "Suwantawiwat",
            "email": "validemail@example.com",
            "password": "short",
            "confirm_password": "short",
        }

        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())

        self.assertIn("password", serializer.errors)
        self.assertIn(
            "This password is too short. It must contain at least 8 characters.",
            str(serializer.errors["password"]),
        )


class RegisterMissingLastNameTestCase(TestCase):

    def test_register_missing_last_name(self):
        data = {
            "first_name": "Uncharee",
            "last_name": "",  # Last name is missing
            "email": "validemail@example.com",
            "password": "ValidPassword123",
            "confirm_password": "ValidPassword123",
        }

        serializer = RegisterSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("last_name", serializer.errors)
        self.assertEqual(
            serializer.errors["last_name"][0], "This field may not be blank."
        )


class RegisterEmptyFieldsTestCase(TestCase):

    def test_register_empty_fields(self):
        data = {
            "first_name": "",
            "last_name": "",
            "email": "",
            "password": "",
            "confirm_password": "",
        }

        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("first_name", serializer.errors)
        self.assertIn(
            "This field may not be blank.", str(serializer.errors["first_name"])
        )

        self.assertIn("last_name", serializer.errors)
        self.assertIn(
            "This field may not be blank.", str(serializer.errors["last_name"])
        )

        self.assertIn("email", serializer.errors)
        self.assertIn("This field may not be blank.", str(serializer.errors["email"]))

        self.assertIn("password", serializer.errors)
        self.assertIn(
            "This field may not be blank.", str(serializer.errors["password"])
        )

        self.assertIn("confirm_password", serializer.errors)
        self.assertIn(
            "This field may not be blank.", str(serializer.errors["confirm_password"])
        )


# study preference test
class StudyPreferenceValidInputTestCase(TestCase):

    def test_study_preference_valid_data(self):
        data = {
            "chronotype": "early_bird",
            "concentration": "high",
            "studying_style": "solo",
            "procrastination": True,
            "physical_activity": "Regular exercise",
        }

        serializer = StudyPreferenceSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)


class StudyPreferenceMissingFieldsTestCase(TestCase):

    def test_study_preference_missing_fields(self):
        data = {
            "chronotype": "morning",
        }

        serializer = StudyPreferenceSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("concentration", serializer.errors)
        self.assertIn("studying_style", serializer.errors)
        self.assertIn("procrastination", serializer.errors)
        self.assertIn("physical_activity", serializer.errors)


class StudyPreferenceInvalidDataTypeTestCase(TestCase):

    def test_study_preference_invalid_data_type(self):
        data = {
            "chronotype": "morning",
            "concentration": 100,
            "studying_style": "visual",
            "procrastination": "low",
            "physical_activity": "active",
        }

        serializer = StudyPreferenceSerializer(data=data)

        self.assertFalse(serializer.is_valid())

        self.assertIn("concentration", serializer.errors)
        self.assertIn("is not a valid choice.", str(serializer.errors["concentration"]))


class LoginTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="Keepypie47@gmail.com",
            first_name="Existing",
            last_name="User",
        )
        self.user.set_password("Keepypie11")
        self.user.save()

        # print(f"User created: {self.user.email}")
        # print(
        #     f"Hashed password: {self.user.password}"
        # )

    def test_valid_login(self):
        data = {
            "email": "Keepypie47@gmail.com",
            "password": "Keepypie11",
        }
        response = self.client.post("/auth/token/", data, format="json")
        # print(f"response status: {response.status_code}")
        # print(f"response data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_password(self):
        data = {
            "email": "Keepypie47@gmail.com",
            "password": "Keepypie",
        }
        response = self.client.post("/auth/token/", data, format="json")
        print(f"response status: {response.status_code}")
        print(f"response data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

    def test_nonexistent_user(self):
        data = {
            "email": "Kokocrunch@gmail.com",
            "password": "Keepypie11",
        }
        response = self.client.post("/auth/token/", data, format="json")
        # print(f"response status: {response.status_code}")
        # print(f"response data: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)

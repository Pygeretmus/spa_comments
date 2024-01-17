from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def setUp(self):
        user = User.objects.create(
            email="test1@gmail.com",
            username="test1",
            first_name="test1_name",
            last_name="test1_surname",
            password=make_password("string"),
        )
        User.objects.create(
            email="test2@gmail.com",
            username="test2",
            first_name="test2_name",
            last_name="test2_surname",
            password=make_password("string"),
        )
        self.client.force_authenticate(user)

    # -------------------------------------LIST ALL USERS-------------------------------------------
    def test_user_list_wrong_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="Authentication credentials were not provided.", code="not_authenticated"
            ),
        )

    def test_user_list_success(self):
        response = self.client.get(reverse("user-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # -------------------------------------RETRIEVE USER--------------------------------------------
    def test_user_retrieve_wrong_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("user-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="Authentication credentials were not provided.", code="not_authenticated"
            ),
        )

    def test_user_retrieve_wrong_not_found(self):
        response = self.client.get(reverse("user-detail", args=[3]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], ErrorDetail(string="Not found.", code="not_found")
        )

    def test_user_retrieve_success(self):
        response = self.client.get(reverse("user-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "email": "test1@gmail.com",
                "username": "test1",
                "first_name": "test1_name",
                "last_name": "test1_surname",
            },
        )

    # ---------------------------------------CREATE USER--------------------------------------------
    def test_user_create_wrong_email_required(self):
        response = self.client.post(
            reverse("user-list"),
            data={
                "username": "test3",
                "password": "string",
                "confirm": "string",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["email"], [ErrorDetail(string="This field is required.", code="required")]
        )

    def test_user_create_wrong_username_required(self):
        response = self.client.post(
            reverse("user-list"),
            data={
                "email": "test3@gmail.com",
                "password": "string",
                "confirm": "string",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["username"],
            [ErrorDetail(string="This field is required.", code="required")],
        )

    def test_user_create_wrong_password_required(self):
        response = self.client.post(
            reverse("user-list"),
            data={
                "email": "test3@gmail.com",
                "username": "test2",
                "confirm": "string",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password"],
            [ErrorDetail(string="This field is required.", code="required")],
        )

    def test_user_create_wrong_confirm_required(self):
        response = self.client.post(
            reverse("user-list"),
            data={"email": "test3@gmail.com", "username": "test3", "password": "string"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["confirm"],
            [ErrorDetail(string="This field is required.", code="required")],
        )

    def test_user_create_wrong_confirm_not_match(self):
        response = self.client.post(
            reverse("user-list"),
            data={
                "email": "test3@gmail.com",
                "username": "test3",
                "password": "string",
                "confirm": "notstring",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [ErrorDetail(string="Password and confirm do not match.", code="invalid")],
        )

    def test_user_create_wrong_email_exist(self):
        response = self.client.post(
            reverse("user-list"),
            data={
                "email": "test2@gmail.com",
                "username": "test3",
                "password": "string",
                "confirm": "string",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [ErrorDetail(string="Email already exists.", code="invalid")],
        )

    def test_user_create_wrong_username_exist(self):
        response = self.client.post(
            reverse("user-list"),
            data={
                "email": "test3@gmail.com",
                "username": "test2",
                "password": "string",
                "confirm": "string",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [ErrorDetail(string="Username already exists.", code="invalid")],
        )

    def test_user_create_success(self):
        response = self.client.post(
            reverse("user-list"),
            data={
                "email": "test3@gmail.com",
                "username": "test3",
                "first_name": "test3_name",
                "last_name": "test3_surname",
                "password": "string",
                "confirm": "string",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "id": 3,
                "email": "test3@gmail.com",
                "username": "test3",
                "first_name": "test3_name",
                "last_name": "test3_surname",
            },
        )

        response = self.client.get(reverse("user-list"))
        self.assertEqual(len(self.client.get(reverse("user-list")).data), 3)
        self.assertEqual(
            self.client.get(reverse("user-detail", args=[3])).data,
            {
                "id": 3,
                "email": "test3@gmail.com",
                "username": "test3",
                "first_name": "test3_name",
                "last_name": "test3_surname",
            },
        )

    # ---------------------------------------DESTROY USER-------------------------------------------
    def test_user_destroy_wrong_not_authenticated(self):
        self.client.logout()
        response = self.client.delete(reverse("user-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="Authentication credentials were not provided.", code="not_authenticated"
            ),
        )

    def test_user_destroy_wrong_forbidden(self):
        response = self.client.delete(reverse("user-detail", args=[2]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="You do not have permission to perform this action.",
                code="permission_denied",
            ),
        )

    def test_user_destroy_wrong_not_found(self):
        response = self.client.delete(reverse("user-detail", args=[3]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], ErrorDetail(string="Not found.", code="not_found")
        )

    def test_user_destroy_success(self):
        response = self.client.delete(reverse("user-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    # ---------------------------------------UPDATE USER--------------------------------------------
    def test_user_update_wrong_not_authenticated(self):
        self.client.logout()
        response = self.client.put(reverse("user-detail", args=[3]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="Authentication credentials were not provided.", code="not_authenticated"
            ),
        )

    def test_user_update_wrong_email_exist(self):
        response = self.client.put(
            reverse("user-detail", args=[1]),
            data={
                "email": "test2@gmail.com",
                "username": "nottest1",
                "first_name": "nottest1_name",
                "last_name": "nottest1_surname",
                "password": "notstring",
                "confirm": "notstring",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [ErrorDetail(string="Email already exists.", code="invalid")],
        )

    def test_user_update_wrong_username_exist(self):
        response = self.client.put(
            reverse("user-detail", args=[1]),
            data={
                "email": "nottest1@gmail.com",
                "username": "test2",
                "first_name": "nottest1_name",
                "last_name": "nottest1_surname",
                "password": "notstring",
                "confirm": "notstring",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [ErrorDetail(string="Username already exists.", code="invalid")],
        )

    def test_user_update_wrong_not_found(self):
        response = self.client.put(reverse("user-detail", args=[3]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], ErrorDetail(string="Not found.", code="not_found")
        )

    def test_user_update_wrong_email_required(self):
        response = self.client.put(
            reverse("user-detail", args=[1]),
            data={
                "username": "nottest1",
                "password": "notstring",
                "confirm": "notstring",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["email"], [ErrorDetail(string="This field is required.", code="required")]
        )

    def test_user_update_wrong_username_required(self):
        response = self.client.put(
            reverse("user-detail", args=[1]),
            data={
                "email": "nottest1@gmail.com",
                "password": "notstring",
                "confirm": "notstring",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["username"],
            [ErrorDetail(string="This field is required.", code="required")],
        )

    def test_user_update_wrong_password_required(self):
        response = self.client.put(
            reverse("user-detail", args=[1]),
            data={
                "email": "nottest1@gmail.com",
                "username": "nottest1",
                "confirm": "notstring",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["password"],
            [ErrorDetail(string="This field is required.", code="required")],
        )

    def test_user_update_wrong_confirm_required(self):
        response = self.client.put(
            reverse("user-detail", args=[1]),
            data={
                "email": "nottest1@gmail.com",
                "username": "nottest1",
                "password": "notstring",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["confirm"],
            [ErrorDetail(string="This field is required.", code="required")],
        )

    def test_user_update_wrong_confirm_not_match(self):
        response = self.client.put(
            reverse("user-detail", args=[1]),
            data={
                "email": "nottest1@gmail.com",
                "username": "nottest1",
                "password": "notstring",
                "confirm": "string",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [ErrorDetail(string="Password and confirm do not match.", code="invalid")],
        )

    def test_user_update_wrong_forbidden(self):
        response = self.client.put(reverse("user-detail", args=[2]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="You do not have permission to perform this action.",
                code="permission_denied",
            ),
        )

    def test_user_update_success(self):
        response = self.client.put(
            reverse("user-detail", args=[1]),
            data={
                "email": "nottest1@gmail.com",
                "username": "nottest1",
                "first_name": "nottest1_name",
                "last_name": "nottest1_surname",
                "password": "notstring",
                "confirm": "notstring",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "email": "nottest1@gmail.com",
                "username": "nottest1",
                "first_name": "nottest1_name",
                "last_name": "nottest1_surname",
            },
        )

    # -----------------------------------PARTIAL UPDATE USER----------------------------------------

    def test_user_partial_update_wrong_not_authenticated(self):
        self.client.logout()
        response = self.client.patch(reverse("user-detail", args=[2]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="Authentication credentials were not provided.", code="not_authenticated"
            ),
        )

    def test_user_partial_update_wrong_forbidden(self):
        response = self.client.patch(reverse("user-detail", args=[2]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="You do not have permission to perform this action.",
                code="permission_denied",
            ),
        )

    def test_user_partial_update_wrong_not_found(self):
        response = self.client.patch(reverse("user-detail", args=[3]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], ErrorDetail(string="Not found.", code="not_found")
        )

    def test_user_partial_update_wrong_confirm_not_match(self):
        response = self.client.patch(
            reverse("user-detail", args=[1]),
            data={
                "password": "notstring",
                "confirm": "string",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [ErrorDetail(string="Password and confirm do not match.", code="invalid")],
        )

    def test_user_partial_update_wrong_email_exist(self):
        response = self.client.patch(
            reverse("user-detail", args=[1]),
            data={"email": "test2@gmail.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [ErrorDetail(string="Email already exists.", code="invalid")],
        )

    def test_user_partial_update_wrong_username_exist(self):
        response = self.client.patch(
            reverse("user-detail", args=[1]),
            data={"username": "test2"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["non_field_errors"],
            [ErrorDetail(string="Username already exists.", code="invalid")],
        )

    def test_user_partial_update_success(self):
        response = self.client.patch(
            reverse("user-detail", args=[1]),
            data={"email": "nottest1@gmail.com"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": 1,
                "email": "nottest1@gmail.com",
                "username": "test1",
                "first_name": "test1_name",
                "last_name": "test1_surname",
            },
        )

from commentsapp.models import Comments
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase


class CommentsTests(APITestCase):
    def setUp(self):
        user = User.objects.create(
            email="test1@gmail.com",
            username="test1",
            first_name="test1_name",
            last_name="test1_surname",
            password=make_password("string"),
        )
        comment = Comments.objects.create(
            user=user,
            home="https://google.com",
            text="Let's agree",
        )
        self.client.force_authenticate(user)
        user = User.objects.create(
            email="test2@gmail.com",
            username="test2",
            first_name="test2_name",
            last_name="test2_surname",
            password=make_password("string"),
        )
        Comments.objects.create(user=user, text="to disagree!", reply=comment)

    # -------------------------------------CREATE COMMENT-------------------------------------------
    def test_comment_create_wrong_text_required(self):
        response = self.client.post(
            reverse("comment-list"),
            data={"home": "string", "reply": 0},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["text"], [ErrorDetail(string="This field is required.", code="required")]
        )

    def test_comment_create_success(self):
        response = self.client.post(
            reverse("comment-list"),
            data={"text": "string"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {"id": 3, "user": 1, "text": "string", "home": "", "reply": None, "replies": []},
        )

        self.assertEqual(len(self.client.get(reverse("comment-list")).data), 3)
        self.assertEqual(
            self.client.get(reverse("comment-detail", args=[3])).data,
            {"id": 3, "user": 1, "text": "string", "home": "", "reply": None, "replies": []},
        )

    # -----------------------------------LIST ALL COMMENTS------------------------------------------
    def test_comment_list_wrong_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("comment-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="Authentication credentials were not provided.", code="not_authenticated"
            ),
        )

    def test_comment_list_success(self):
        response = self.client.get(reverse("comment-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    # -----------------------------------RETRIEVE COMMENT-------------------------------------------
    def test_comment_retrieve_wrong_not_authenticated(self):
        self.client.logout()
        response = self.client.get(reverse("comment-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="Authentication credentials were not provided.", code="not_authenticated"
            ),
        )

    def test_comment_retrieve_wrong_not_found(self):
        response = self.client.get(reverse("comment-detail", args=[4]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], ErrorDetail(string="Not found.", code="not_found")
        )

    def test_comment_retrieve_success(self):
        response = self.client.get(reverse("comment-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["home"], "https://google.com")

    # -------------------------------------DESTROY COMMENT------------------------------------------

    def test_comment_destroy_wrong_not_authenticated(self):
        self.client.logout()
        response = self.client.delete(reverse("comment-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="Authentication credentials were not provided.", code="not_authenticated"
            ),
        )

    def test_comment_destroy_wrong_forbidden(self):
        response = self.client.delete(reverse("comment-detail", args=[2]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="You do not have permission to perform this action.",
                code="permission_denied",
            ),
        )

    def test_comment_destroy_wrong_not_found(self):
        response = self.client.delete(reverse("comment-detail", args=[4]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], ErrorDetail(string="Not found.", code="not_found")
        )

    def test_comment_destroy_success(self):
        response = self.client.delete(reverse("comment-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

    # -------------------------------------UPDATE COMMENT-------------------------------------------
    def test_comment_update_wrong_not_authenticated(self):
        self.client.logout()
        response = self.client.put(reverse("comment-detail", args=[3]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="Authentication credentials were not provided.", code="not_authenticated"
            ),
        )

    def test_comment_update_wrong_not_found(self):
        response = self.client.put(reverse("comment-detail", args=[4]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], ErrorDetail(string="Not found.", code="not_found")
        )

    def test_comment_update_wrong_text_required(self):
        response = self.client.put(
            reverse("comment-detail", args=[1]),
            data={"home": "string", "reply": 0},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["text"], [ErrorDetail(string="This field is required.", code="required")]
        )

    def test_comment_update_wrong_forbidden(self):
        response = self.client.put(reverse("comment-detail", args=[2]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="You do not have permission to perform this action.",
                code="permission_denied",
            ),
        )

    def test_comment_update_success(self):
        response = self.client.put(
            reverse("comment-detail", args=[1]),
            data={"text": "Hello!"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["text"], "Hello!")

    # ---------------------------------PARTIAL UPDATE COMMENTS---------------------------------------

    def test_comment_partial_update_wrong_not_authenticated(self):
        self.client.logout()
        response = self.client.patch(reverse("comment-detail", args=[1]))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="Authentication credentials were not provided.", code="not_authenticated"
            ),
        )

    def test_comment_partial_update_wrong_forbidden(self):
        response = self.client.patch(reverse("comment-detail", args=[2]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"],
            ErrorDetail(
                string="You do not have permission to perform this action.",
                code="permission_denied",
            ),
        )

    def test_comment_partial_update_wrong_not_found(self):
        response = self.client.patch(reverse("comment-detail", args=[4]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"], ErrorDetail(string="Not found.", code="not_found")
        )

    def test_comment_partial_update_success(self):
        response = self.client.patch(
            reverse("comment-detail", args=[1]),
            data={"reply": 2},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["reply"], 2)

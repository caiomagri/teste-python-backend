from django.urls import reverse
from faker import Faker

from rest_framework.test import APITestCase, APIClient


class TestSetup(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.register_url = reverse("user-list")
        self.auth_url = reverse("token_obtain_pair")

        self.fake = Faker()

        self.user_data = {
            "username": self.fake.email().split('@')[0],
            "password": self.fake.email(),
            "email": self.fake.email(),
            "first_name": self.fake.name(),
            "last_name": self.fake.name()
        }

        return super(TestSetup, self).setUp()

    def tearDown(self) -> None:
        return super(TestSetup, self).tearDown()

    def get_user_id(self):
        first_user_response = self.client.post(self.register_url, self.user_data, format="json")
        user_id = first_user_response.data.get("id")

        self.authenticate()
        return user_id

    def get_new_user_payload(self):
        return {
            "username": self.fake.email().split('@')[0],
            "password": self.fake.email(),
            "email": self.fake.email(),
            "first_name": self.fake.name(),
            "last_name": self.fake.name()
        }

    def authenticate(self):
        auth_response = self.client.post(self.auth_url, self.user_data)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {auth_response.data.get('access')}")

from rest_framework import status

from .test_setup import TestSetup


class TestAuthViews(TestSetup):
    def test_user_cannot_auth_with_no_data(self):
        response = self.client.post(self.auth_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_auth_with_invalid_credentials(self):
        response = self.client.post(self.auth_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_auth_correctly(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.auth_url, self.user_data)

        self.assertIsInstance(response.data["access"], str)
        self.assertIsInstance(response.data["refresh"], str)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

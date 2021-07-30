from rest_framework import status

from api.core.tests.test_setup import TestSetup


class CreateUserViews(TestSetup):

    def test_user_cannot_register_with_no_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register_correctly(self):
        response = self.client.post(self.register_url, self.user_data, format="json")

        self.assertEqual(response.data["username"], self.user_data["username"])
        self.assertEqual(response.data["email"], self.user_data["email"])
        self.assertEqual(response.data["first_name"], self.user_data["first_name"])
        self.assertEqual(response.data["last_name"], self.user_data["last_name"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_cannot_register_with_duplicated_username(self):
        self.client.post(self.register_url, self.user_data, format="json")
        response = self.client.post(self.register_url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ListUserViews(TestSetup):

    def test_user_cannot_list_without_aut(self):
        self.client.post(self.register_url, self.user_data, format="json")

        response = self.client.get(self.register_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_list(self):
        created_user = self.client.post(self.register_url, self.user_data, format="json")
        self.authenticate()

        response = self.client.get(self.register_url, format="json")

        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)

        user = response.data[0]

        self.assertEqual(user.get("id"), created_user.data.get("id"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UpdateUserViews(TestSetup):

    def test_user_cannot_update_without_auth(self):
        user_id = self.get_user_id()

        self.client.credentials(HTTP_AUTHORIZATION=None)

        response = self.client.put(f"{self.register_url}{user_id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update_with_no_data(self):
        user_id = self.get_user_id()

        response = self.client.put(f"{self.register_url}{user_id}/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_update_others_users(self):
        self.get_user_id()
        other_user = self.client.post(self.register_url, self.get_new_user_payload(), format="json")
        other_user_id = other_user.data.get("id")

        update_payload = {
            "email": self.fake.email(),
            "first_name": self.fake.name(),
            "last_name": self.fake.name()
        }

        response = self.client.put(f"{self.register_url}{other_user_id}/", update_payload)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_update_correctly(self):
        user_id = self.get_user_id()

        update_payload = {
            "email": self.fake.email(),
            "first_name": self.fake.name(),
            "last_name": self.fake.name()
        }

        response = self.client.put(f"{self.register_url}{user_id}/", update_payload)

        self.assertEqual(response.data["email"], update_payload["email"])
        self.assertEqual(response.data["first_name"], update_payload["first_name"])
        self.assertEqual(response.data["last_name"], update_payload["last_name"])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_update_password_without_old_password(self):
        user_id = self.get_user_id()

        update_payload = {
            "password": self.fake.email(),
        }

        response = self.client.put(f"{self.register_url}{user_id}/", update_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_update_password_with_wrong_old_password(self):
        user_id = self.get_user_id()

        update_payload = {
            "password": self.fake.email(),
            "old_password": self.fake.email(),
        }

        response = self.client.put(f"{self.register_url}{user_id}/", update_payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_update_password_correctly(self):
        user_id = self.get_user_id()

        update_payload = {
            "password": self.fake.email(),
            "old_password": self.user_data.get("password"),
        }

        response = self.client.put(f"{self.register_url}{user_id}/", update_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DeleteUserViews(TestSetup):

    def test_user_cannot_delete_without_auth(self):
        user_id = self.get_user_id()

        self.client.credentials(HTTP_AUTHORIZATION=None)

        response = self.client.delete(f"{self.register_url}{user_id}/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_others_users(self):
        self.get_user_id()
        other_user = self.client.post(self.register_url, self.get_new_user_payload(), format="json")
        other_user_id = other_user.data.get("id")

        response = self.client.delete(f"{self.register_url}{other_user_id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_delete_correctly(self):
        user_id = self.get_user_id()

        response = self.client.delete(f"{self.register_url}{user_id}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

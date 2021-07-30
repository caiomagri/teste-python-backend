from django.urls import reverse
from rest_framework import status

from api.core.tests.test_setup import TestSetup


class LotteryResultViews(TestSetup):

    def test_lottery_result_cannot_list_without_aut(self):
        self.client.post(self.register_url, self.user_data, format="json")

        response = self.client.get(reverse('lottery_result'), format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lottery_result_can_list_correct(self):
        self.get_user_id()

        response = self.client.get(reverse('lottery_result'), format="json")

        self.assertIsInstance(response.data['result'], list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateBetViews(TestSetup):
    def test_bets_cannot_create_without_aut(self):
        self.client.post(self.register_url, self.user_data, format="json")

        response = self.client.post(reverse('bets'), format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bets_cannot_create_with_dozens_without_between_six_and_ten(self):
        self.get_user_id()

        payload = {
            "dozens": 1
        }

        response = self.client.post(reverse('bets'), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bets_can_create_correctly(self):
        self.get_user_id()

        payload = {"dozens": 10}

        response = self.client.post(reverse('bets'), payload, format="json")

        self.assertIsInstance(response.data['numbers'], list)
        self.assertEqual(len(response.data['numbers']), payload.get("dozens"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ListBetViews(TestSetup):

    def test_bets_cannot_list_without_aut(self):
        self.client.post(self.register_url, self.user_data, format="json")

        response = self.client.get(reverse('bets'), format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bets_can_list_correctly(self):
        self.get_user_id()
        payload = {"dozens": 10}
        bet_created = self.client.post(reverse('bets'), payload, format="json")

        response = self.client.get(reverse('bets'), format="json")

        self.assertIsInstance(response.data, list)

        bet = response.data[0]

        self.assertEqual(bet.get("id"), bet_created.data.get("id"))
        self.assertEqual(bet.get("numbers"), bet_created.data.get("numbers"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetBetResultViews(TestSetup):

    def test_bets_result_cannot_get_without_aut(self):
        self.client.post(self.register_url, self.user_data, format="json")

        response = self.client.get(reverse('last_bet_result'), format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bets_result_cannot_list_without_one_bet(self):
        self.get_user_id()

        response = self.client.get(reverse('last_bet_result'), format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bets_result_can_list_correct(self):
        self.get_user_id()

        payload = {"dozens": 10}

        self.client.post(reverse('bets'), payload, format="json")

        response = self.client.get(reverse('last_bet_result'), format="json")

        self.assertIsInstance(response.data['result'], list)
        self.assertIsInstance(response.data['numbers'], list)
        self.assertIsInstance(response.data['right_numbers'], dict)
        self.assertIsInstance(response.data['right_numbers']['total_right'], int)
        self.assertIsInstance(response.data['right_numbers']['numbers'], list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

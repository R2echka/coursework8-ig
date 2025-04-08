from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase

from habbits.models import Habbit
from users.models import User


# Create your tests here.
class HabbitTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create(email="meow@meow.meow")
        self.client.force_authenticate(user=self.user)
        self.habbit = Habbit.objects.create(
            time="12:00",
            owner=self.user,
            action="something",
            is_enjoyable=False,
            time_to_complete=120,
            periodicity=7,
            reward="test",
        )

    def test_create_habbit(self):
        data = {
            "time": "00:00",
            "action": "meow",
            "is_enjoyable": "True",
            "time_to_complete": 90,
            "periodicity": 3,
        }
        response = self.client.post("/habbit/", data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            response.json(),
            {
                "id": 1,
                "place": None,
                "time": "00:00:00",
                "action": "meow",
                "is_enjoyable": True,
                "periodicity": 3,
                "reward": None,
                "time_to_complete": 90,
                "is_public": False,
                "owner": 1,
                "related_habbit": None,
            },
        )

    def test_create_habbit_failed(self):
        data = {
            "time": "01:00",
            "action": "something",
            "is_enjoyable": "True",
            "time_to_complete": 180,
            "periodicity": 3,
        }
        self.client.post("/habbit/", data=data)

        self.assertRaises(ValidationError)

    def test_view_habbits(self):
        response = self.client.get("/habbit/")
        response1 = self.client.get(f"/habbit/{self.habbit.pk}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

    def test_view_habbit_failed(self):
        response = self.client.get("/habbit/0/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_habbit(self):
        data = {
            "time": "12:00",
            "action": "something",
            "is_enjoyable": False,
            "periodicity": 7,
            "reward": "test",
            "time_to_complete": 120,
            "is_public": True,
        }
        response = self.client.put(f"/habbit/{self.habbit.pk}/", data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            response.json(),
            {
                "id": self.habbit.pk,
                "place": None,
                "time": "12:00:00",
                "action": "something",
                "is_enjoyable": True,
                "periodicity": 3,
                "reward": "test",
                "time_to_complete": 120,
                "is_public": True,
                "related_habbit": None,
                "owner": self.user,
            },
        )

    def test_public_habbits(self):
        response = self.client.get("/habbit/public_habbits/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_habbit(self):
        response = self.client.delete(f"/habbit/{self.habbit.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_lesson_failed(self):
        response = self.client.delete("/habbit/0/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

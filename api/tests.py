from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from api.serializers import ImportSerializer
from .models import Import, Citizen

import_data = {
    'citizens': [{
        "citizen_id": 1,
        "town": "Москва",
        "street": "Льва Толстого",
        "building": "16к7стр5",
        "apartment": 7,
        "name": "Иванов Иван Иванович",
        "birth_date": "26.12.1986",
        "gender": "male",
        "relatives": [2]
    }, {
        "citizen_id": 2,
        "town": "Москва",
        "street": "Льва Толстого",
        "building": "16к7стр5",
        "apartment": 7,
        "name": "Иванов Сергей Иванович",
        "birth_date": "17.04.1997",
        "gender": "male",
        "relatives": [1]
    }, {
        "citizen_id": 3,
        "town": "Керчь",
        "street": "Иосифа Бродского",
        "building": "2",
        "apartment": 11,
        "name": "Романова Мария Леонидовна",
        "birth_date": "23.11.1986",
        "gender": "female",
        "relatives": []
    }]
}


class CreateImportTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('import-list')

    def create_import(self):
        return self.client.post(self.url, import_data)

    def test_response(self):
        response = self.create_import()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'data': {'import_id': 1}})

    def test_created_instances(self):
        self.create_import()

        self.assertEqual(Import.objects.count(), 1)
        self.assertEqual(Citizen.objects.count(), 3)

    def test_citizen_relations(self):
        self.create_import()

        citizen1 = Citizen.objects.get(citizen_id=1)
        citizen2 = Citizen.objects.get(citizen_id=2)
        citizen3 = Citizen.objects.get(citizen_id=3)

        self.assertEqual(citizen1.relatives.count(), 1)
        self.assertEqual(citizen2.relatives.count(), 1)
        self.assertEqual(citizen3.relatives.count(), 0)

        self.assertEqual(citizen1.relatives.first(), citizen2)
        self.assertEqual(citizen2.relatives.first(), citizen1)

    def test_invalid_fields(self):
        data = {
            'citizens': [{
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": None
            }]
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Import.objects.count(), 0)
        self.assertEqual(Citizen.objects.count(), 0)

    def test_invalid_relations(self):
        data = {
            'citizens': [{
                "citizen_id": 1,
                "town": "Москва",
                "street": "Льва Толстого",
                "building": "16к7стр5",
                "apartment": 7,
                "name": "Иванов Иван Иванович",
                "birth_date": "26.12.1986",
                "gender": "male",
                "relatives": [0]
            }]
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Import.objects.count(), 0)
        self.assertEqual(Citizen.objects.count(), 0)


class UpdateCitizenTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('citizen', kwargs={'import_id': 1, 'citizen_id': 1})

        serializer = ImportSerializer(data=import_data)
        serializer.is_valid()
        serializer.save()

    def test_response(self):
        response = self.client.patch(self.url, {'name': 'Иванов Иван Сергеевич'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'data': {
            "citizen_id": 1,
            "town": "Москва",
            "street": "Льва Толстого",
            "building": "16к7стр5",
            "apartment": 7,
            "name": "Иванов Иван Сергеевич",
            "birth_date": "26.12.1986",
            "gender": "male",
            "relatives": [2]
        }})

    def test_relations(self):
        self.client.patch(self.url, {'relatives': [3]})

        citizen1 = Citizen.objects.get(citizen_id=1)
        citizen2 = Citizen.objects.get(citizen_id=2)
        citizen3 = Citizen.objects.get(citizen_id=3)

        self.assertEqual(citizen1.relatives.first(), citizen3)
        self.assertEqual(citizen2.relatives.count(), 0)
        self.assertEqual(citizen3.relatives.first(), citizen1)

    def test_citizen_id_update(self):
        response = self.client.patch(self.url, {'citizen_id': 4})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Citizen.objects.filter(citizen_id=1).count(), 1)
        self.assertEqual(Citizen.objects.filter(citizen_id=4).count(), 0)

    def test_empty_input_update(self):
        response = self.client.patch(self.url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_null_values_update(self):
        response = self.client.patch(self.url, {'name': None})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_found(self):
        response = self.client.patch(reverse('citizen', kwargs={'import_id': 1, 'citizen_id': 10}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetCitizenListTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        serializer = ImportSerializer(data=import_data)
        serializer.is_valid()
        serializer.save()

    def test_response(self):
        url = reverse('citizen-list', kwargs={'import_id': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'data': import_data['citizens']})

    def test_not_found(self):
        url = reverse('citizen-list', kwargs={'import_id': 2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetBirthdayGifts(APITestCase):
    @classmethod
    def setUpTestData(cls):
        serializer = ImportSerializer(data=import_data)
        serializer.is_valid()
        serializer.save()

    def test_response(self):
        url = reverse('birthdays', kwargs={'import_id': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'data': {
            '1': [],
            '2': [],
            '3': [],
            '4': [{'citizen_id': 1, 'presents': 1}],
            '5': [],
            '6': [],
            '7': [],
            '8': [],
            '9': [],
            '10': [],
            '11': [],
            '12': [{'citizen_id': 2, 'presents': 1}],
        }})

    def test_not_found(self):
        url = reverse('birthdays', kwargs={'import_id': 2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAgePercentileTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        serializer = ImportSerializer(data=import_data)
        serializer.is_valid()
        serializer.save()

    def test_response(self):
        url = reverse('age-percentile', kwargs={'import_id': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'data': [
            {
                'town': 'Москва',
                'p50': 27,
                'p75': 29,
                'p99': 31
            },
            {
                'town': 'Керчь',
                'p50': 32,
                'p75': 32,
                'p99': 32
            }
        ]})

    def test_not_found(self):
        url = reverse('age-percentile', kwargs={'import_id': 2})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

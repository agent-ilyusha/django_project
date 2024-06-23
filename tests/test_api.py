import datetime
import os
import uuid

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status

from app.models import Address, Car, ServiceRecord, Owner


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reminder.settings')


def create_viewset_test(model_class, url, creation_attrs):
    class ViewSetTest(TestCase):
        def setUp(self):
            """
            Setup view set.
            :return:
            """
            self.client = APIClient()
            self.user = User.objects.create_user(
                username='test',
                password='test_1234',
                is_staff=True,
            )
            self.superuser = User.objects.create_user(
                username='super_test',
                password='test_1234',
                is_superuser=True,
            )
            self.user_token = Token.objects.create(user=self.user)
            self.superuser_token = Token.objects.create(user=self.superuser)

        def get(self, user: User, token: Token):
            """
            Authenticate user.
            :param user:
            :param token:
            :return:
            """
            self.client.force_authenticate(user=user, token=token)
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

        def test_get_by_user(self):
            """
            Test by user.
            :return:
            """
            self.get(self.user, self.user_token)

        def test_get_by_superuser(self):
            """
            Test by superuser.
            :return:
            """
            self.get(self.superuser, self.superuser_token)

        def manage(self, user: User, token: Token, post_status: int, put_status: int, delete_status: int):
            """
            Test that a user can manage their own records.
            :param user:
            :param token:
            :param post_status:
            :param put_status:
            :param delete_status:
            :return:
            """
            self.client.force_authenticate(user=user, token=token)

            # creating object
            created_id = model_class.objects.create(**creation_attrs).id

            # post
            response = self.client.post(url, creation_attrs)
            self.assertEqual(response.status_code, post_status)

            # put
            response = self.client.put(f'{url}{created_id}/', creation_attrs)
            self.assertEqual(response.status_code, put_status)

            # delete
            response = self.client.delete(f'{url}{created_id}/')
            self.assertEqual(response.status_code, delete_status)

        def test_manage_user(self):
            self.manage(
                self.user, self.user_token,
                post_status=status.HTTP_403_FORBIDDEN,
                put_status=status.HTTP_403_FORBIDDEN,
                delete_status=status.HTTP_403_FORBIDDEN,
            )

        def test_manage_superuser(self):
            self.manage(
                self.superuser, self.superuser_token,
                post_status=status.HTTP_201_CREATED,
                put_status=status.HTTP_200_OK,
                delete_status=status.HTTP_204_NO_CONTENT,
            )

    return ViewSetTest


data_address = {
    'country': 'Russian',
    'city': 'Sochi',
    'street': 'San-Francisco',
    'num_house': 19,
    'housing': 3,
}

data_car = {
    'mark': 'Nissan',
    'model': 'Skyline',
    'price': 9000,
    'date_of_issue': '2001-09-12',
}

data_owner = {
    'name': 'Ilya',
    'surname': 'Na',
    'patronymic': 'Patronymic',
    'number': '85782243648',
}

data_serviceRecord = {
    'type_work': 'settings',
    'price': 9000,
    'the_date_of_the': '2001-01-01',
}

AddressViewSetTest = create_viewset_test(Address, '/rest/addresses/', data_address)
CarViewSetTest = create_viewset_test(Car, '/rest/cars/', data_car)
OwnerViewSetTest = create_viewset_test(Owner, '/rest/owners/', data_owner)
ServiceRecordViewSetTest = create_viewset_test(ServiceRecord, '/rest/services/', data_serviceRecord)

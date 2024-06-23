"""
Model testing module.
"""
import parameterized
from django.contrib.auth.models import User

from app.models import *
from app.constant import *
from django.db import models
from django.test import TestCase
from parameterized import parameterized_class

import datetime
import unittest


data_owner = [
    (
        {
            'id': [1, True],
            'name': ['Ilya', True],
            'surname': ['Na', True],
            'patronymic': ['Patronymic', True],
            'number': ['85782243648', True],
            'money': [123, True],
        }, True
    ),
    (
        {
            'id': [2, True],
            'name': ['Ilya1', False],
            'surname': ['Na', True],
            'patronymic': ['Patronymic', True],
            'number': ['85782243648', True],
            'money': [123, True],
        }, False
    )
]

data_car = [
    (
        {
            'id': [1, True],
            'mark': ['Nissan', True],
            'model': ['Skyline', True],
            'date_of_issue': ['2005-01-01', True],
            'price': [9000, True],
        }, True
    ),
    (
        {
            'id': [2, True],
            'mark': ['Москвич', True],
            'model': ['3', False],
            'date_of_issue': ['2005-01-01', True],
            'price': [-9000, False],
        }, False
    )
]

data_service_record = [
    (
        {
            'id': [1, True],
            'type_work': ['settings', True],
            'price': [9000, True],
            'the_date_of_the': ['2005-01-01', True],
        }, True
    ),
    (
        {
            'id': [2, True],
            'type_work': ['settings', True],
            'price': [9000, True],
            'the_date_of_the': ['2035-01-01', False],
        }, False
    )
]

data_address = [
    (
        {
            'id': [1, True],
            'country': ['Russian', True],
            'city': ['Sochi', True],
            'street': ['San-Francisco', True],
            'num_house': [19, True],
            'housing': [33, True],
        }, True
    ),
    (
        {
            'id': [1, True],
            'country': ['Russian', True],
            'city': ['Sochi123', False],
            'street': ['San-Francisco', True],
            'num_house': [19, True],
            'housing': [33, True],
        }, False
    )
]


def test_max_length_data(name_field: str, model_db: [models.Model, UUIDMixin], flag: bool, id_data: int) -> None:
    model = model_db.objects.get(id=id_data)
    max_length = model._meta.get_field(name_field).max_length
    assert len(getattr(model, name_field)) <= max_length, flag


def test_data(name_fields: str, model_db: [models.Model, UUIDMixin], flag: bool, id_data: int) -> None:
    model = model_db.objects.get(id=id_data)
    unittest.TestCase().assertEqual(first=getattr(model, name_fields).isalpha(), second=flag)


def test_date_of_issue_label(name_fields: str, model_db: [models.Model, UUIDMixin], flag: bool, id_data: int) -> None:
    model = model_db.objects.get(id=id_data)
    unittest.TestCase().assertEqual(
        datetime.date.fromisoformat(str(getattr(model, name_fields))) <= datetime.date.today(), flag)


def test_max_price(name_fields: str, model_db: [models.Model, UUIDMixin], max_price: int, flag: bool,
                   id_data: int) -> None:
    model = model_db.objects.get(id=id_data)
    unittest.TestCase().assertEqual(0 <= getattr(model, name_fields) <= max_price, flag)


def test_max_number_label(name_field: str, max_number: int, flag: bool, id_data: int) -> None:
    addr = Address.objects.get(id=id_data)
    unittest.TestCase().assertEqual(getattr(addr, name_field) <= max_number, flag)


@parameterized_class(('data', 'expected'), data_owner)
class OwnerModelTest(TestCase):
    """
    Test model owner functionality.
    """

    def setUp(self):
        """
        Setup test cases.
        :return:
        """
        self.client = User.objects.create_user('test_owner', 'test')
        self.id_data = self.data.get("id")[0]
        self.flags_to_fields = {field: val[1] for field, val in self.data.items()}
        Owner.objects.create(**{field: val[0] for field, val in self.data.items()})

    def test_name_label(self) -> None:
        """
        Check that the name label works.
        :return:
        """
        test_data('name', Owner, self.flags_to_fields.get('name'), self.id_data)

    def test_surname_label(self) -> None:
        """
        Check that the surname label works.
        :return:
        """
        test_data('surname', Owner, self.flags_to_fields.get('surname'), self.id_data)

    def test_patronymic_label(self) -> None:
        """
        Check that the patronymic label works.
        :return:
        """
        test_data('patronymic', Owner, self.flags_to_fields.get('patronymic'), self.id_data)

    def test_max_length_name_label(self) -> None:
        """
        Check that the max_length name label works.
        :return:
        """
        test_max_length_data('name', Owner, self.flags_to_fields.get('name'), self.id_data)

    def test_surname_max_length_name_label(self) -> None:
        """
        Check that the surname max length name label works.
        :return:
        """
        test_max_length_data('surname', Owner, self.flags_to_fields.get('surname'), self.id_data)

    def test_max_length_patronymic_label(self) -> None:
        """
        Check that the max length patronymic label works.
        :return:
        """
        test_max_length_data('patronymic', Owner, self.flags_to_fields.get('patronymic'), self.id_data)

    def test_min_length_number_label(self) -> None:
        """
        Check that the min length number label works.
        :return:
        """
        owner = Owner.objects.get(id=self.id_data)
        self.assertEquals(
            MIN_LENGTH_NUMBER_PHONE <= len(owner.number) <= MAX_NUMBER_HOUSE,
            self.flags_to_fields.get('number')
        )

    def test_number_phone_label_on_isalnum(self) -> None:
        """
        Check that the number phone label on isalnum label works.
        :return:
        """
        owner = Owner.objects.get(id=self.id_data)
        self.assertEquals(owner.number.isalnum(), self.flags_to_fields.get('number'))

    def test_money_label(self) -> None:
        """
        Check that the money label works.
        :return:
        """
        owner = Owner.objects.get(id=self.id_data)
        self.assertEquals(owner.money > 0, self.flags_to_fields.get('money'))


@parameterized_class(('data', 'expected'), data_car)
class CarModelTest(TestCase):
    """
    Test model car functionality.
    """

    def setUp(self):
        """
        Setup test cases.
        :return:
        """
        self.client = User.objects.create_user('test_owner', 'test')
        self.id_data = self.data.get("id")[0]
        self.flags_to_fields = {field: val[1] for field, val in self.data.items()}
        Car.objects.create(**{field: val[0] for field, val in self.data.items()})

    def test_mark_label(self) -> None:
        """
        Check that the mark label works.
        :return:
        """
        test_data('mark', Car, self.flags_to_fields.get('mark'), self.id_data)

    def test_model_label(self) -> None:
        """
        Check that the model label works.
        :return:
        """
        test_data('model', Car, self.flags_to_fields.get('model'), self.id_data)

    def test_max_length_mark_label(self) -> None:
        """
        Check max length mark label.
        :return:
        """
        test_max_length_data('mark', Car, self.flags_to_fields.get('mark'), self.id_data)

    def test_model_modelCar_max_length(self) -> None:
        """
        Check max length model car label.
        :return:
        """
        test_max_length_data('model', Car, self.flags_to_fields.get('model'), self.id_data)

    def test_date_of_issue_label(self) -> None:
        """
        Check that the date of issue label works.
        :return:
        """
        test_date_of_issue_label('date_of_issue', Car, self.flags_to_fields.get('date_of_issue'), self.id_data)

    def test_price(self):
        """
        Check that the price label works.
        :return:
        """
        test_max_price('price', Car, MAX_PRICE_CAR, self.flags_to_fields.get('price'), self.id_data)

    def test_description_label(self) -> None:
        """
        Check that the description label works.
        :return:
        """
        car = Car.objects.get(id=self.id_data)
        self.assertEquals(len(car.description) <= MAX_LENGTH_DESCRIPTION_FIELD, True)


@parameterized_class(('data', 'expected'), data_address)
class AddressModelTest(TestCase):
    """
    Test model address functionality.
    """

    def setUp(self):
        """
        Setup test cases.
        :return:
        """
        self.client = User.objects.create_user('test_owner', 'test')
        self.id_data = self.data.get("id")[0]
        self.flags_to_fields = {field: val[1] for field, val in self.data.items()}
        Address.objects.create(**{field: val[0] for field, val in self.data.items()})

    def test_country_label(self) -> None:
        """
        Check that the country label works.
        :return:
        """
        test_data('country', Address, self.flags_to_fields.get('country'), self.id_data)

    def test_city_label(self) -> None:
        """
        Check that the city label works.
        :return:
        """
        test_data('city', Address, self.flags_to_fields.get('city'), self.id_data)

    def test_max_length_country_label(self) -> None:
        """
        Check max length country label.
        :return:
        """
        test_data('country', Address, self.flags_to_fields.get('country'), self.id_data)

    def test_max_length_city_label(self) -> None:
        """
        Check max length city label.
        :return:
        """
        test_max_length_data('city', Address, self.flags_to_fields.get('city'), self.id_data)

    def test_max_length_street_label(self) -> None:
        """
        Check max length street label.
        :return:
        """
        test_max_length_data('street', Address, self.flags_to_fields.get('street'), self.id_data)

    def test_max_number_num_house_label(self) -> None:
        """
        Check max number number of house label.
        :return:
        """
        test_max_number_label('num_house', MAX_NUMBER_HOUSE, self.flags_to_fields.get('num_house'), self.id_data)

    def test_max_number_housing_label(self) -> None:
        """
        Check max number of housing label.
        :return:
        """
        test_max_number_label('housing', MAX_NUMBER_HOUSING, self.flags_to_fields.get('housing'), self.id_data)


@parameterized_class(('data', 'expected'), data_service_record)
class ServiceRecordModelTest(TestCase):
    """
    Test model service record functionality.
    """

    def setUp(self):
        """
        Setup test cases.
        :return:
        """
        self.client = User.objects.create_user('test_owner', 'test')
        self.id_data = self.data.get("id")[0]
        self.flags_to_fields = {field: val[1] for field, val in self.data.items()}
        ServiceRecord.objects.create(**{field: val[0] for field, val in self.data.items()})

    def test_validation_price(self):
        """
        Check that the price label works.
        :return:
        """
        test_max_price('price', ServiceRecord, MAX_PRICE_SERVICE_RECORD, self.flags_to_fields.get('price'),
                       self.id_data)

    def test_max_length_type_work_label(self) -> None:
        """
        Check max length type label.
        :return:
        """
        test_max_length_data('type_work', ServiceRecord, self.flags_to_fields.get('type_work'), self.id_data)

    def test_date_the_date_of_the_label(self) -> None:
        """
        Check that the date of label works.
        :return:
        """
        test_date_of_issue_label('the_date_of_the', ServiceRecord, self.flags_to_fields.get('the_date_of_the'),
                                 self.id_data)


for owner, car, address, srevice_record in zip(data_owner, data_car, data_address, data_service_record):
    setattr(OwnerModelTest, 'data', owner)
    setattr(CarModelTest, 'data', car)
    setattr(AddressModelTest, 'data', address)
    setattr(ServiceRecordModelTest, 'data', srevice_record)

    if __name__ == "__main__":
        unittest.main()

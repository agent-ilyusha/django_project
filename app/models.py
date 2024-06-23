import datetime

from django.conf.global_settings import AUTH_USER_MODEL

from app import constant

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from string import digits, punctuation, whitespace
from uuid import uuid4


def check_on_letter(letters: str):
    """
    Checks if something other than letters is used.
    :param letters:
    :return:
    """
    letters = set(letters)
    punctuations = set(punctuation)
    digit = set(digits)
    whitespaces = set(whitespace)
    if letters & punctuations or letters & digit or letters & whitespaces:
        raise ValidationError('Invalid letters!')


def check_on_variable_date(str_date: str):
    """
    Checks date validity.
    :param str_date:
    :return:
    """
    if datetime.date.fromisoformat(str(str_date)) > datetime.date.today():
        raise ValidationError('Invalid date!')


def check_on_variable_number(number: str):
    """
    Checks number validity.
    :param number:
    :return:
    """
    if not number.isalnum() and constant.MIN_LENGTH_NUMBER_PHONE <= len(number) <= constant.MAX_LENGTH_NUMBER_PHONE:
        raise ValidationError("Number is too long or small")


class UUIDMixin(models.Model):
    """
    Id for models.
    """
    id: models.UUIDField = models.UUIDField(primary_key=True, default=uuid4, editable=False, null=False)

    class Meta:
        abstract = True
        unique_together = ['id']


class Owner(UUIDMixin):
    """
    List owner model.
    """
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    name: models.CharField = models.CharField(
        _('name'),
        max_length=constant.MAX_LENGTH_OWNER_FIELDS,
        null=False,
        validators=[check_on_letter]
    )
    surname: models.CharField = models.CharField(
        _('surname'),
        max_length=constant.MAX_LENGTH_OWNER_FIELDS,
        null=False,
        validators=[check_on_letter]
    )
    patronymic: models.CharField = models.CharField(
        _('patronymic'),
        max_length=constant.MAX_LENGTH_OWNER_FIELDS,
        null=True,
        blank=True,
        validators=[check_on_letter]
    )
    money: models.FloatField = models.FloatField(
        _('money'),
        null=True,
        default=0,
        validators=[
            MinValueValidator(0)
        ]
    )
    number: models.CharField = models.CharField(
        _('number'),
        null=True,
        blank=True,
        validators=[
            check_on_variable_number
        ])

    cars = models.ManyToManyField('Car', through='CarToOwner', verbose_name=_('cars'))
    addresses = models.ManyToManyField('Address', through='OwnerToAddress', verbose_name=_('addresses'))

    class Meta:
        verbose_name = _('owner')
        verbose_name_plural = _('owners')

    def __str__(self):
        return f'Owner: \
        {self.name}, \
        {self.surname}, \
        {self.patronymic if self.patronymic else ""}, \
        {self.number if self.number else ""}.'


class ServiceRecord(UUIDMixin):
    """
    List ServiceRecord model.
    """
    type_work: models.TextField = models.CharField(
        _('type_work'),
        max_length=constant.MAX_LENGTH_TYPE_WORK,
        null=False
    )
    price: models.FloatField = models.FloatField(
        _('price'),
        null=False,
        validators=[
            MaxValueValidator(constant.MAX_PRICE_SERVICE_RECORD),
            MinValueValidator(0)
        ])
    the_date_of_the: models.DateField = models.DateField(
        _('the_date_of_the'),
        null=False,
        validators=[check_on_variable_date]
    )

    car_id: models.ManyToManyField = models.ManyToManyField(
        'Car',
        through='CarToServiceRecord',
        verbose_name=_('car_id'),
    )

    class Meta:
        verbose_name = _('serviceRecord')
        verbose_name_plural = _('serviceRecords')

    def get_dict(self):
        return {'type_work': self.type_work, 'price': self.price, 'the_date_of_the': self.the_date_of_the}

    def __str__(self):
        return f'{self.type_work} {self.price} {self.the_date_of_the}'


class Car(UUIDMixin):
    """
    list Car model.
    """
    mark: models.CharField = models.CharField(
        _('name'),
        max_length=constant.MAX_LENGTH_CAR_FIELDS,
        null=False
    )
    model: models.CharField = models.CharField(
        _('model'),
        max_length=constant.MAX_LENGTH_CAR_FIELDS,
        null=False
    )
    date_of_issue: models.DateField = models.DateField(
        _('year_of_issue'),
        null=False,
        validators=[check_on_variable_date]
    )
    price: models.FloatField = models.FloatField(
        _('price'),
        null=False,
        validators=[
            MaxValueValidator(constant.MAX_PRICE_CAR),
            MinValueValidator(0)
        ]
    )

    description: models.TextField = models.TextField(
        _('description'),
        max_length=constant.MAX_LENGTH_DESCRIPTION_FIELD,
        null=False
    )

    service_record_id: models.ManyToManyField = models.ManyToManyField(
        ServiceRecord,
        through='CarToServiceRecord',
        verbose_name=_('service_record_id')
    )

    for_sale: models.BooleanField = models.BooleanField(
        _('for_sale'),
        null=False,
        default=False,
    )

    owners = models.ManyToManyField(Owner, through='CarToOwner', verbose_name=_('owners'))

    class Meta:
        verbose_name = _('car')
        verbose_name_plural = _('cars')

    def __str__(self) -> str:
        return f'Car: {self.mark}, \
            {self.model}, \
            {self.date_of_issue}, \
            {self.price}, \
            {self.description}.'

    def __repr__(self):
        return {
            'mark': self.mark,
            'model': self.model,
            'date_of_issue': self.date_of_issue,
            'description': self.description if self.description else 'Нет описания',
            'price': self.price if self.price else 0,
        }


class CarToServiceRecord(UUIDMixin):
    car_id: models.UUIDField = models.ForeignKey(Car, on_delete=models.CASCADE)
    service_id: models.UUIDField = models.ForeignKey(ServiceRecord, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.car_id} {self.service_id}'

    class Meta:
        verbose_name = _('carToServiceRecord')
        verbose_name_plural = _('carToServiceRecords')


class Address(UUIDMixin):
    """
    list Address model.
    """
    country: models.CharField = models.CharField(
        _('country'),
        max_length=constant.MAX_LENGTH_ADDRESS_FIELDS,
        null=False,
        validators=[check_on_letter])
    city: models.CharField = models.CharField(_('city'),
                                              max_length=constant.MAX_LENGTH_ADDRESS_FIELDS,
                                              null=False,
                                              validators=[
                                                  check_on_letter
                                              ])
    street: models.CharField = models.CharField(
        _('street'),
        max_length=constant.MAX_LENGTH_ADDRESS_FIELDS,
        null=False
    )
    num_house: models.IntegerField = models.PositiveIntegerField(
        _('num_house'),
        null=False,
        validators=[
            MaxValueValidator(constant.MAX_NUMBER_HOUSE)
        ])
    housing: models.IntegerField = models.PositiveIntegerField(
        _('housing'),
        null=True,
        blank=True,
        validators=[
            MaxValueValidator(constant.MAX_NUMBER_HOUSING)
        ])

    owners = models.ManyToManyField(Owner, through='OwnerToAddress', verbose_name=_('owners'))

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('addresses')

    def __str__(self):
        return f'Address: \
        {self.country}, \
        {self.city}, \
        {self.street}, \
        {self.num_house}, \
        {self.housing if self.housing else ""}'


class OwnerToAddress(UUIDMixin):
    """
    list OwnerToAddress model.
    """
    owner_id: models.ForeignKey = models.ForeignKey('Owner', on_delete=models.CASCADE)
    address_id: models.ForeignKey = models.ForeignKey('Address', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('ownerToAddress')
        verbose_name_plural = _('ownerToAddresses')

    def __str__(self) -> str:
        return f'{self.owner_id} {self.address_id}'


class CarToOwner(UUIDMixin):
    """
    list CarToOwner model.
    """
    car_id: models.ForeignKey = models.ForeignKey(Car, on_delete=models.CASCADE)
    owner_id: models.ForeignKey = models.ForeignKey(Owner, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('carToOwner')
        verbose_name_plural = _('carToOwners')

    def __str__(self) -> str:
        return f'{self.car_id} {self.owner_id}'

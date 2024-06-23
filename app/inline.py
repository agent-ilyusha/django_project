from django.contrib import admin
from app.models import Car, Address, ServiceRecord, Owner, OwnerToAddress, CarToOwner, CarToServiceRecord


class OwnerInline(admin.TabularInline):
    model = Owner


class OwnerToAddressInline(admin.TabularInline):
    model = OwnerToAddress
    extra = 1


class AddressInline(admin.TabularInline):
    model = Address
    extra = 1


class ServiceRecordInline(admin.TabularInline):
    model = ServiceRecord
    extra = 1


class CarInline(admin.TabularInline):
    model = Car
    extra = 1


class CarToOwnerInline(admin.TabularInline):
    model = CarToOwner
    extra = 1


class CarToServiceRecordInline(admin.TabularInline):
    model = CarToServiceRecord
    extra = 1

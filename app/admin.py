from django.contrib import admin
from app.models import Car, Owner, Address, ServiceRecord
from app.inline import OwnerToAddressInline, CarToOwnerInline, CarToServiceRecordInline


class OwnerAdmin(admin.ModelAdmin):
    model = Owner
    inlines = (OwnerToAddressInline, CarToOwnerInline)


class AddressAdmin(admin.ModelAdmin):
    model = Address


class ServiceRecordAdmin(admin.ModelAdmin):
    model = ServiceRecord


class CarAdmin(admin.ModelAdmin):
    model = Car
    inlines = (CarToOwnerInline, CarToServiceRecordInline)


# Registering models in the admin panel
admin.site.register(Address, AddressAdmin)  # address model
admin.site.register(Owner, OwnerAdmin)  # owner model
admin.site.register(ServiceRecord, ServiceRecordAdmin)  # service record model
admin.site.register(Car, CarAdmin)  # car model

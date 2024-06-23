from rest_framework import viewsets, permissions
from rest_framework.authentication import TokenAuthentication, BasicAuthentication

from app.serializers_models import *


class MyPermission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in ('GET', 'OPTIONS', 'HEAD'):
            return bool(request.user and request.user.is_authenticated)
        elif request.method in ('POST', 'DELETE', 'PUT'):
            return bool(request.user and request.user.is_superuser)
        return False


def create_viewset(model_class, serializer):
    class ViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serializer
        authentication_classes = [BasicAuthentication, TokenAuthentication]
        permission_classes = [MyPermission]

    return ViewSet


CarViewSet = create_viewset(Car, CarSerializers)
OwnerViewSet = create_viewset(Owner, OwnerSerializers)
ServiceRecordViewSet = create_viewset(ServiceRecord, ServiceRecordSerializers)
AddressViewSet = create_viewset(Address, AddressSerializers)


def create_user(validated_data):
    user = UserModel.objects.create_user(
        username=validated_data['username'],
        password=validated_data['password'],
    )
    return user

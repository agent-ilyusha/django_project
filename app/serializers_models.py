from rest_framework import serializers
from app.models import Car, Owner, Address, ServiceRecord
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class CarSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ['mark', 'model', 'price', 'date_of_issue', 'service_record_id']


class OwnerSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Owner
        fields = ['name', 'surname', 'patronymic', 'number']


class AddressSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'city', 'street', 'num_house', 'housing']


class ServiceRecordSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ServiceRecord
        fields = ['type_work', 'price', 'the_date_of_the']


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ("username", "password", )

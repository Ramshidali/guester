from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from api.v1.general.functions import get_otp
from customers.models import Customer, Otp
from general.functions import get_auto_id

from general.models import Phone

UserModel = get_user_model()


class RegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=50)
    location = serializers.CharField(max_length=100)
    latitude = serializers.CharField(max_length=200)
    longitude = serializers.CharField(max_length=200)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

    def create(self, validated_data):
        user = UserModel.objects.create_user(validated_data['username'], validated_data['password'])
        return user


class OtpVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Otp
        exclude = ['otp']

    def verify_otp(self, validated_data):
        otp = validated_data['otp']
        phone = validated_data['phone']
        # print(phone)
        # print(otp)
        customerOtp = Otp.objects.get(phone=phone)
        if customerOtp.otp == otp:
            return True
        else:
            return False

    def updateOtp(self, phone,otp):
        # phone = validated_data['phone']

        # otp = get_otp()
        if Otp.objects.filter(phone=phone).exists():
            Otp.objects.filter(phone=phone).update(otp=otp)

        return otp


class RegisterCustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
        otp = Otp.objects.get(phone=validated_data['username'])

        if not validated_data['password']:
            return "Error"

        user = UserModel.objects.create_user(validated_data['username'], validated_data['password'])
        auto_id = get_auto_id(Customer)
        creator = user
        updater = user
        user = Customer.objects.create(user=user, phone=validated_data['username'],
                                       otp=otp.otp, auto_id=auto_id, creator=creator, updater=updater)
        return user


class CustomerSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = fields = ['name','phone','location','latitude','longitude','photo']

    def get_photo(self, instance):
        if instance.photo :
            request = self.context.get('request')
            image_url = instance.photo.url
            return request.build_absolute_uri(image_url)
        else:
            None
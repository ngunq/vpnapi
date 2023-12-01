from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

from api.models import AppUser


class UserRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(max_length=100, required=True)
    last_name = serializers.CharField(max_length=100, required=True)
    user_type = serializers.IntegerField(default=1)
    password = serializers.CharField(write_only=True)
    password1 = ''
    password2 = ''

    class Meta:
        model = AppUser
        fields = [
            'first_name',
            'last_name',
            'user_type'
        ]
    
    def validate(self, data):
        data['password1'] = data['password']
        return data
    
    @transaction.atomic
    def save(self, request):
        user = super().save(request)
        user.user_type = self.validated_data.get('user_type')
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.save()
        return user


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(validators=[validate_password])
    id = serializers.UUIDField()

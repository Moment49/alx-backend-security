from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
        read_only_fields = ['id', 'full_name']

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password= attrs.get('confirm_password')

        if len(password) and len(confirm_password) < 7:
            raise serializers.ValidationError("Password must be above 7 characters")
        else:
            if password != confirm_password:
                raise serializers.ValidationError("Password does not match")
            
        return attrs

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'principal_currency']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,validators=[validate_password],style={'input_type':'password'})
    password_confirm = serializers.CharField(write_only=True,validators=[validate_password])
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'principal_currency']

        extra_kwargs = {
            'principal_currency': {"required":True},
            'password': {"required":True},
            'password_confirm': {"required":True},
        }

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("Email already exists"))
        return email

    def validate(self,attrs):
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError("Passwords don't match")
        return attrs

    def create(self,validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User.objects.create_user(
            password = password,
            **validated_data)
        return user


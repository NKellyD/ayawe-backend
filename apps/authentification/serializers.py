from django.contrib.auth import get_user_model,authenticate
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models.user_email import UserEmail

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
        fields = ['username', 'email', 'first_name', 'last_name', 'principal_currency', 'password', 'password_confirm']

        extra_kwargs = {
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

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True,required=True)
    password = serializers.CharField(write_only=True,required=True,style={'input_type':'password'})

    user = None

    def validate(self,attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            try:
                user_obj = User.objects.get(username=username)
            except User.DoesNotExist:
                try:
                    user_obj = User.objects.get(email=username)
                except User.DoesNotExist:
                    raise serializers.ValidationError(_("No user found with this username or email"))

            user = authenticate(username=user_obj.email, password=password)
            if not user:
                raise serializers.ValidationError(_("Incorrect username or password"))
            self.user = user
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(_("Please enter username and password"))


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = ['id', 'email','is_primary', 'is_active', 'is_verified','created_at']
        read_only_fields = ['id', 'is_active', 'is_verified', 'created_at']

class AddUserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    is_primary = serializers.BooleanField(default=False)

class SetPrimaryEmailSerializer(serializers.Serializer):
    email_id = serializers.IntegerField()









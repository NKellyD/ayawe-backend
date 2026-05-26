from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions,status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from .models import UserEmail
from apps.authentification.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserLoginSerializer,
    UserEmailSerializer,
    AddUserEmailSerializer,
    SetPrimaryEmailSerializer
)
from rest_framework.decorators import action

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": _("User created successfully"),
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            "message": _("User login successfully"),
            "result": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "principal_currency": user.principal_currency
            },
            "tokens": {
                "access": str(access_token),
                "refresh": str(refresh),
            }
        }, status=status.HTTP_200_OK)

class UserEmailView(ModelViewSet):
    queryset = User.objects.prefetch_related('emails')
    serializer_class = None
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='add-email')
    def add_email(self, request):
        serializer = AddUserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.user.add_email(
            user=request.user,
            email=serializer.validated_data['email'],
            is_primary=serializer.validated_data['is_primary'],
        )
        return Response({
            "message": _("Email address added successfully"),
            "result": {
                "email": email.email,
                "is_primary": email.is_primary,
            }
        },
            status=status.HTTP_201_CREATED
        )




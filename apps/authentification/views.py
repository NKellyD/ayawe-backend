from django.contrib.auth import get_user_model
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from .models.user_email import UserEmail
from apps.authentification.serializers import (
    UserRegisterSerializer,
    UserSerializer,
    UserLoginSerializer,
    UserEmailSerializer,
    AddUserEmailSerializer
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
    serializer_class = UserEmailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserEmail.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = AddUserEmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = request.user.add_email(
            email=serializer.validated_data['email'],
            is_primary=serializer.validated_data['is_primary'],
        )
        return Response({
                "message": _("Email added successfully"),
                "object": {
                    "email": email.email,
                    "is_primary": email.is_primary,
                }
        })

    @action(detail=True, methods=["post"], url_path="set-primary")
    def set_primary(self, request, pk=None):
        email = self.get_object()

        request.user.set_primary_email(email.id)

        return Response({
            "message": _("Primary email updated successfully")
        })






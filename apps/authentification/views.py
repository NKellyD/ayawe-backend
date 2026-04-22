from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions,status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _

from apps.authentification.serializers import UserRegisterSerializer, UserSerializer, UserLoginSerializer

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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


from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions,status
from rest_framework.response import Response

from apps.users.serializers import UserRegisterSerializer, UserSerializer

User = get_user_model()

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User created successfully",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED)


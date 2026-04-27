from .models import Account
from .serializers import AccountSerializer
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.utils.translation import gettext_lazy as _


class AccountView(generics.GenericAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        account = serializer.save()

        return Response({
            'message': (_('Account successfully created.')),
            'result': AccountSerializer(account).data
        },status=status.HTTP_201_CREATED)

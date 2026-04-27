from unicodedata import category

from .models.account import Account
from .models.category import CategoryType,Category
from .serializers import AccountSerializer,CategorySerializer,CategoryTypeSerializer
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

class CategoryTypeView(generics.GenericAPIView):
    queryset = CategoryType.objects.all()
    serializer_class = CategoryTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category_type = serializer.save()

        return Response({
            'message': (_('Category Type successfully created.')),
            'result': CategoryTypeSerializer(category_type).data
        },status=status.HTTP_201_CREATED)

class CategoryView(generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = serializer.save()
        return Response({
            'message': (_('Category successfully created.')),
            'result': CategorySerializer(category).data
        },status=status.HTTP_201_CREATED)







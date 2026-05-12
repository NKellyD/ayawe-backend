from unicodedata import category

from .models.account import Account
from .models.category import Category
from .serializers import AccountSerializer,CategorySerializer
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView


class AccountView(generics.ListCreateAPIView):
    queryset = Account.objects.all().order_by('-id')
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

class CategoryTypeListView(APIView):
    def get(self, request):
        data = [
            {"value": key, "label": label}
            for key, label in Category.TYPE_CHOICES
        ]
        return Response(data)

class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('-id')
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







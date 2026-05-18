from .models.account import Account
from .models.category import Category
from .models.contribution import Contribution
from .models.target import Target
from .serializers import AccountSerializer,CategorySerializer,TargetSerializer,ContributionSerializer
from rest_framework.response import Response
from rest_framework import status, generics, permissions, viewsets, request
from django.utils.translation import gettext_lazy as _
from rest_framework.views import APIView


class AccountView(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Account.objects.all()
        else:
            return Account.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)



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


class TargetView(viewsets.ModelViewSet):
    serializer_class = TargetSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.is_staff:
            return Target.objects.filter()
        else:
            return Target.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ContributionView(viewsets.ModelViewSet):
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Contribution.objects.select_related('target','created_by')
        if self.request.user.is_staff:
            return queryset
        else:
            return queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)






from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models.account import Account
from .models.category import Category

User = get_user_model()

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'name', 'amount', 'currency', 'type_account', 'date_created']
        read_only_fields = ['date_created']

    def create(self, validated_data):
        user = self.context['request'].user

        if not validated_data.get('currency'):
            validated_data['currency'] = user.principal_currency

        validated_data['user'] = user
        return super().create(validated_data)


class CategorySerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'type_display', 'icon_name']
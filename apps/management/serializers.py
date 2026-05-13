from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from datetime import date
from .models.account import Account
from .models.category import Category
from .models.target import Target
from .models.contribution import Contribution

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

class ContributionSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    class Meta:
        model = Contribution
        fields = [
            'id',
            'target',
            'contribution_date',
            'created_by',
            'created_by_username',
            'amount_to_contributed',
            'description',
        ]
        read_only_fields = ['id','created_by','contribution_date']

    def validate(self, data):
        target = data.get('target')
        amount = data.get('amount_to_contributed')

        future_amount = target.amount_saved + amount

        if future_amount > target.target_amount:
            raise serializers.ValidationError(_("Target amount cannot be greater than amount saved"))

        if amount <= 0:
            raise serializers.ValidationError(_("Target must be greater than 0"))

        if target.end_target_date < date.today():
            raise serializers.ValidationError(_("Target date expired"))

        return data

class TargetSerializer(serializers.ModelSerializer):

    contributions = ContributionSerializer(
        many=True,
        read_only=True
    )

    amount_saved = serializers.ReadOnlyField()
    remaining_amount = serializers.ReadOnlyField()
    progress_percentage = serializers.ReadOnlyField()

    class Meta:
        model = Target
        fields = [
            'id',
            'name',
            'target_amount',
            'initial_amount',
            'amount_saved',
            'remaining_amount',
            'progress_percentage',
            'contributions',
            'created_at',
            'start_target_date',
            'end_target_date'
        ]
        read_only_fields = [
            'created_at',
            'start_target_date',
            'contributions',
            'amount_saved',
            'remaining_amount',
            'progress_percentage',
        ]
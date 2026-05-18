import uuid

from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from datetime import date
from uuid import uuid4
from .models.account import Account
from .models.category import Category
from .models.target import Target
from .models.contribution import Contribution

User = get_user_model()

class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = ['id', 'name', 'amount', 'currency', 'type_account','account_number','is_active', 'date_created','updated_at']
        read_only_fields = ['date_created','updated_at']

    def validate(self, data):
        type_account = data.get('type_account',getattr(self.instance, 'type_account', None))
        account_number = data.get('account_number',getattr(self.instance, 'account_number', None))

        if type_account == Account.TypeAccounts.MOBILE:
            if not account_number:
                raise serializers.ValidationError(_("Account number is required"))
        return data

    def create(self, validated_data):
        user = self.context['request'].user

        if not validated_data.get('currency'):
            validated_data['currency'] = user.principal_currency

        type_account = validated_data.get('type_account',getattr(self.instance, 'type_account', None))
        if type_account == Account.TypeAccounts.BANK:
            validated_data['account_number'] = (
                f"BANK_{uuid.uuid4().hex[:6].upper()}"
            )

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

        # if not target:
        #     raise serializers.ValidationError(_({"target": "Target is required"}))
        #
        # if amount is None:
        #     raise serializers.ValidationError(_({"amount": "Amount is required"}))


        if amount <= 0:
            raise serializers.ValidationError(_("Target must be greater than 0"))

        future_amount = target.amount_saved + amount

        if future_amount > target.target_amount:
            raise serializers.ValidationError(_("Target amount cannot be greater than amount saved"))


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
from django.db import models
from decimal import Decimal

from ayawe import settings

User = settings.AUTH_USER_MODEL

class Account(models.Model):
    class CurrencyTypes(models.TextChoices):
        BIF = 'BIF', 'Franc Burundais'
        USD = 'USD', 'Dollar US'
        EUR = 'EUR', 'Euro'


    class TypeAccounts(models.TextChoices):
        CASH = 'CASH', 'Cash'
        MOBILE = 'MOBILE', 'Mobile'
        BANK = 'BANK', 'Bank'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=Decimal('0.00'))
    account_number = models.CharField(max_length=100, blank=True, null=True,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(choices=CurrencyTypes.choices, max_length=50,default=CurrencyTypes.BIF)
    type_account = models.CharField(choices=TypeAccounts.choices, max_length=50,default=TypeAccounts.CASH)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'name'],
                name='unique_user_account_name',
            )
        ]




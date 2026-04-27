from django.db import models

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
        Bank = 'BANK', 'Bank'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(choices=CurrencyTypes.choices, max_length=50,blank=True, null=True)
    type_account = models.CharField(choices=TypeAccounts.choices, max_length=50,default=TypeAccounts.CASH)

    def __str__(self):
        return self.name



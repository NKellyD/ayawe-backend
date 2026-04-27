from django.db import models

from ayawe import settings

User = settings.AUTH_USER_MODEL

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account')
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    class CurrencyTypes(models.TextChoices):
        BIF = 'BIF', 'BIF'
        USD = 'USD', 'USD'
        EUR = 'EUR', 'EUR'
    currency = models.CharField(choices=CurrencyTypes.choices, max_length=50,blank=True, null=True)

    def __str__(self):
        return self.name



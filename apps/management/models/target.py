from django.contrib.auth import get_user_model
from django.db import models
from decimal import Decimal
from django.db.models import Sum

User = get_user_model()

class Target(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_user')
    name = models.CharField(max_length=200,unique=True)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    target_amount = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    start_target_date = models.DateField(auto_now_add=True)
    end_target_date = models.DateField(blank=True, null=True)

    @property
    def amount_saved(self):
        contributions_total = self.contributions.aggregate(
            total=Sum('amount_to_contributed'))['total'] or Decimal(0.0)

        return self.initial_amount + contributions_total


    @property
    def remaining_amount(self):
        return self.target_amount - self.amount_saved

    @property
    def progress_percentage(self):
        if self.target_amount <= 0:
            return 0
        else:
            return round((self.amount_saved / self.target_amount) * 100, 2)

    class Meta:
        ordering = ['id']






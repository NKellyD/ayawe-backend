from django.contrib.auth import get_user_model
from django.db import models
from datetime import date

User = get_user_model()

class Target(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='target_user')
    name = models.CharField(max_length=200,unique=True)
    target_amount = models.DecimalField(max_digits=10,decimal_places=2)
    total_amount_saved = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    start_target_date = models.DateField()
    end_target_date = models.DateField()

    @property
    def amount_saved(self):
        return self.total_amount_saved

    @property
    def amount_target(self):
        return self.target_amount

    @property
    def end_date(self):
        return self.end_target_date

    def target_contribution_saved(self, amount):
        return self.total_amount_saved + amount





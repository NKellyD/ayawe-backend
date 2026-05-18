from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .target import Target

User = get_user_model()

class Contribution(models.Model):
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name='contributions')
    contribution_date = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contributions_created_by')
    amount_to_contributed = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()


    def __str__(self):
        return str(self.target.name)

    class Meta:
        ordering = ['id']


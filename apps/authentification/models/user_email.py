from django.db.models import Q
from django.db import models
from django.conf import settings

class UserEmail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField(unique=True)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['id']
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(is_primary=True),
                name='unique_primary_email_per_user',
            )
        ]

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models,transaction
from django.core.exceptions import ValidationError
from apps.authentification.managers import UserManager
from .user_email import UserEmail

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    class CurrencyTypes(models.TextChoices):
        BIF = 'BIF', 'Franc Burundais'
        USD = 'USD', 'Dollar US'
        EUR = 'EUR', 'Euro'
    principal_currency = models.CharField(choices=CurrencyTypes.choices, max_length=50,default=CurrencyTypes.BIF)
    two_factor_enabled = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    EMAIL_FIELD = 'email'

    def __str__(self):
        return self.username

    @transaction.atomic
    def add_email(self, email, is_primary=False):
        if UserEmail.objects.filter(email=email).exists():
            raise ValidationError('Email address already in use')
        if is_primary:
            self.emails.update(is_primary=False)
        user_email = UserEmail.objects.create(user=self,email=email, is_primary=is_primary)
        if is_primary:
            self.email = email
            self.save(update_fields=['email'])

        return user_email

    @transaction.atomic
    def set_primary_email(self, email_id):
        try:
            email_obj = UserEmail.objects.get(id=email_id)
        except UserEmail.DoesNotExist:
            raise ValidationError('Email not found')
        self.emails.update(is_primary=False)
        email_obj.is_primary = True
        email_obj.save(update_fields=['is_primary'])
        self.email = email_obj.email
        self.save(update_fields=['email'])
        return email_obj




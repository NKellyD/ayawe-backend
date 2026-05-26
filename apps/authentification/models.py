from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models,transaction
from django.core.exceptions import ValidationError
from django.db.models import Q

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(email, username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


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
        if self.emails.filter(email=email).exists():
            raise ValidationError('Email address already in use')
        if is_primary:
            self.emails.update(is_primary=False)
        return UserEmail.objects.create(user=self,email=email, is_primary=is_primary)

    @transaction.atomic
    def set_email_primary(self, email_id):
        self.emails.update(is_primary=False)
        email = self.emails.get(id=email_id)
        email.is_primary = True
        email.save()
        return email




class UserEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField(unique=True)
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(is_primary=True),
                name='unique_primary_email_per_user',
            )
        ]


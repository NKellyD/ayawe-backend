from django.contrib.auth.models import BaseUserManager
from apps.authentification.models.user_email import UserEmail

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        UserEmail.objects.create(user=user, email=email, is_primary=True)
        return user
    def create_superuser(self, email, username, password, **extra_fields):
        user = self.create_user(email, username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user
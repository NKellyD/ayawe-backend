from django.db import models

class Category(models.Model):
    EXPENSE = 'expense'
    INCOME = 'income'

    TYPE_CHOICES = [
        (EXPENSE, 'Dépense'),
        (INCOME, 'Revenu'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    icon_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

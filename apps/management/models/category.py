from django.db import models

class CategoryType(models.Model):
    class CategoryTypeName(models.TextChoices):
        EXPENSES = 'E', 'Expenses'
        INCOMES = 'I', 'Incomes'
    name = models.CharField(choices=CategoryTypeName.choices,max_length=255,default=CategoryTypeName.EXPENSES)
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    icon_name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

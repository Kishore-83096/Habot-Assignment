from django.db import models

# Create your models here.

from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)  # required
    email = models.EmailField(unique=True)   # required & unique
    department = models.CharField(max_length=50, blank=True, null=True)
    role = models.CharField(max_length=50, blank=True, null=True)
    date_joined = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


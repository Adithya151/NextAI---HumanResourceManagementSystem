from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('Admin', 'Admin'),
        ('Employee', 'Employee'),
        ('Manager', 'Manager'),
        ('Recruiter', 'Recruiter'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Employee')  # ✅ fixed


    def __str__(self):
        return f"{self.username} ({self.role})"

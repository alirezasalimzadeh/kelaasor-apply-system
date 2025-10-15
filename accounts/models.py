from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    DEGREE_CHOICES = (
        ("diploma", "Diploma"),
        ("associate", "Associate Degree"),
        ("bachelor", "Bachelor's Degree"),
        ("master", "Master's Degree"),
        ("phd", "PhD"),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    national_id = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=15)
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES)
    gpa = models.FloatField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

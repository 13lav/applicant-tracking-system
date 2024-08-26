from django.db import models

# Create your models here.

class Applicant(models.Model):
    STATUS_CHOICES = [
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('applied', 'Applied'),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    years_of_exp = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    current_salary = models.IntegerField()
    expected_salary = models.IntegerField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='applied')

    def __str__(self):
        return self.name

from django.db import models

# Create your models here.
class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    date_of_birth = models.DateField()
    enrollment_date = models.DateField()
    course = models.CharField(max_length=100)
    gpa = models.DecimalField(max_digits=3, decimal_places=2)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
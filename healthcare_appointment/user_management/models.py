from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from role_management.models import Role

# Create your models here.
def get_default_role():
    return Role.objects.get(title=settings.DEFAULT_ROLE_NAME)

class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True, default=get_default_role)

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=100)
    qualifications = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.specialty}"


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    medical_history = models.TextField()
    insurance_details = models.TextField()

    def __str__(self):
        return self.user.username


class Availability(models.Model):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='availabilities')
    day_of_week = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('doctor', 'day_of_week', 'start_time', 'end_time')

    def __str__(self):
        return f"{self.doctor.user.username} - {self.day_of_week} {self.start_time}-{self.end_time}"


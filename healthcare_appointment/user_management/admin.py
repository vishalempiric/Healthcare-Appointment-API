from django.contrib import admin
from .models import User, DoctorProfile, PatientProfile, Availability

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'first_name', 'last_name', 'username', 'email', 'is_active', 'date_joined']


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'specialty', 'qualifications']


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__']


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'day_of_week', 'start_time', 'end_time']


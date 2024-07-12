from django.contrib import admin
from .models import Appointment


# Register your models here.
@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        "patient",
        "doctor",
        "status",
        "requested_at",
        "approved_at",
        "date",
        "start_time",
        "end_time",
    ]

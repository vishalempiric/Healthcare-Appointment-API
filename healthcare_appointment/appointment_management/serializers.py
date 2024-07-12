from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'status', 'requested_at', 'approved_at', 'date', 'start_time', 'end_time']
        read_only_fields = ['status', 'requested_at', 'approved_at', 'date', 'start_time', 'end_time']


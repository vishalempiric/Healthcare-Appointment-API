from datetime import datetime, timedelta
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from user_management.models import Availability
from .serializers import AppointmentSerializer


class CreateAppointmentView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(patient=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ApproveAppointmentView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        if appointment.status != 'pending':
            return Response({"error": "Appointment is not in a pending state."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check doctor's availability
        doctor_availabilities = Availability.objects.filter(doctor=appointment.doctor)
        existing_appointments = Appointment.objects.filter(
            doctor=appointment.doctor,
            status='approved',
            date__gte=datetime.now().date()
        )

        for availability in doctor_availabilities:
            start_time = datetime.combine(availability.day_of_week, availability.start_time)
            end_time = datetime.combine(availability.day_of_week, availability.end_time)
            
            # Check for overlapping appointments
            overlap = existing_appointments.filter(
                Q(date=availability.day_of_week) &
                (
                    Q(start_time__lt=end_time) & Q(end_time__gt=start_time)
                )
            ).exists()

            if not overlap:
                # Schedule appointment
                appointment.status = 'approved'
                appointment.date = availability.day_of_week
                appointment.start_time = availability.start_time
                appointment.end_time = availability.end_time
                appointment.approved_at = datetime.now()
                appointment.save()

                return Response(AppointmentSerializer(appointment).data, status=status.HTTP_200_OK)

        return Response({"error": "No available slots found."}, status=status.HTTP_400_BAD_REQUEST)

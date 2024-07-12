from django.urls import path
from . import views

urlpatterns = [
    path('create_appointment/', views.CreateAppointmentView.as_view(), name='create-appointment'),
    path('approve_appointment/<int:appointment_id>/', views.ApproveAppointmentView.as_view(), name='approve-appointment'),
]

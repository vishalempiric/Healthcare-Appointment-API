# Django Imports
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.utils import timezone

# Django Rest Framework Imports
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

# Local Imports
from .models import DoctorProfile, PatientProfile, User
from .serializers import (
    DoctorProfileSerializer,
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    PatientProfileSerializer,
    UserSerializer,
)
from healthcare_appointment.utils import handle_exception


# Create your views here.
class UserRegistrationView(views.APIView):

    @handle_exception
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)


class UserLoginView(views.APIView):

    def get_jwt_tokens(self, user):
        refresh_token = RefreshToken.for_user(user)
        return {"refresh_token": str(refresh_token), "access_token": str(refresh_token.access_token)}

    @handle_exception
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get("username")
        password = serializer.data.get("password")
        user = authenticate(request, username=username, password=password)
        
        if not user:
            return Response({"error": "Invalid Username or Password"}, status=status.HTTP_404_NOT_FOUND)

        jwt_tokens = self.get_jwt_tokens(user)
        login(request, user)
        return Response({"message": "User login successfully", "token": jwt_tokens}, status=status.HTTP_200_OK)


class UserCRUDAPIView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @handle_exception
    def get(self, request, id):
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def patch(self, request, id):
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def put(self, request, id):
        user = get_object_or_404(User, pk=id)
        serializer = UserSerializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception
    def delete(self, request, id):
        user = get_object_or_404(User, pk=id)
        user.is_deleted = True
        user.deleted_at = timezone.now()
        user.deleted_by = request.user
        user.save()
        return Response({"message": "User Deleted successfully", "status": status.HTTP_200_OK})


class PasswordResetRequestView(views.APIView):

    @handle_exception
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(views.APIView):

    @handle_exception
    def post(self, request, uidb64, token, *args, **kwargs):
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(User, pk=uid)

        if user and default_token_generator.check_token(user, token):
            serializer = PasswordResetConfirmSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token or user ID."}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(views.APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @handle_exception
    def patch(self, request):
        if request.user.role.title == 'doctor':
            doctor_profile = get_object_or_404(DoctorProfile, user=request.user)
            serializer = DoctorProfileSerializer(doctor_profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        elif request.user.role.title == 'patient':
            patient_profile = get_object_or_404(PatientProfile, user=request.user)
            serializer = PatientProfileSerializer(patient_profile, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    @handle_exception 
    def get(self, request):
        if request.user.role.title == 'doctor':
            doctor_profile = get_object_or_404(DoctorProfile, user=request.user)
            serializer = DoctorProfileSerializer(doctor_profile)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        elif request.user.role.title == 'patient':
            patient_profile = get_object_or_404(PatientProfile, user=request.user)
            serializer = PatientProfileSerializer(patient_profile)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)


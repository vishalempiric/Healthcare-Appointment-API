from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserCRUDAPIView.as_view(), name="usercrud"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('register/', views.UserRegistrationView.as_view(), name="login"),
    path('<int:id>/', views.UserCRUDAPIView.as_view(), name="usercruddetail"),
    path('password-reset/', views.PasswordResetRequestView.as_view(), name='password_reset'),
    path('reset-password-confirm/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]

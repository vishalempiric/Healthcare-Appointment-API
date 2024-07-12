from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .models import DoctorProfile, PatientProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = getattr(instance, 'role', None)
        if role.title == 'doctor':
            try:
                DoctorProfile.objects.create(user=instance)
            except Exception as e:
                print(f"Error creating DoctorProfile: {e}")
        elif role.title == 'patient':
            try:
                PatientProfile.objects.create(user=instance)
            except Exception as e:
                print(f"Error creating PatientProfile: {e}")
    
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    role = getattr(instance, 'role', None)
    if role.title == 'doctor':
        try:
            instance.doctor_profile.save()
        except ObjectDoesNotExist:
            print("DoctorProfile does not exist for this user.")
        except Exception as e:

            print(f"Error saving DoctorProfile: {e}")
    elif role.title == 'patient':
        try:
            instance.patient_profile.save()
        except ObjectDoesNotExist:
            print("PatientProfile does not exist for this user.")
        except Exception as e:
            print(f"Error saving PatientProfile: {e}")

# from django.db.models.signals import post_save
# from django.dispatch import receiver

# from .models import AcademicSession, AcademicTerm


# @receiver(post_save, sender=AcademicSession)
# def after_saving_session(sender, created, instance, *args, **kwargs):
#     """Change all academic sessions to false if this is true"""
#     if instance.current is True:
#         AcademicSession.objects.exclude(pk=instance.id).update(current=False)


# @receiver(post_save, sender=AcademicTerm)
# def after_saving_term(sender, created, instance, *args, **kwargs):
#     """Change all academic terms to false if this is true."""
#     if instance.current is True:
#         AcademicTerm.objects.exclude(pk=instance.id).update(current=False)


# # signals.py

# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver
# from .models import Profile

# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()




##### updated for deploy render

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, AcademicSession, AcademicTerm


# Signal for AcademicSession
@receiver(post_save, sender=AcademicSession)
def after_saving_session(sender, instance, created, **kwargs):
    """Ensure only one AcademicSession is marked as current."""
    if instance.current:  # True is implicit
        AcademicSession.objects.exclude(pk=instance.id).update(current=False)


# Signal for AcademicTerm
@receiver(post_save, sender=AcademicTerm)
def after_saving_term(sender, instance, created, **kwargs):
    """Ensure only one AcademicTerm is marked as current."""
    if instance.current:  # True is implicit
        AcademicTerm.objects.exclude(pk=instance.id).update(current=False)


# Signal for User - Create Profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Automatically create a Profile when a new User is created."""
    if created:
        try:
            Profile.objects.create(user=instance)
        except Exception as e:
            # Log or handle exceptions for debugging
            print(f"Error creating Profile for User {instance}: {e}")


# Signal for User - Save Profile
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """Save the Profile when the User is saved."""
    try:
        if hasattr(instance, 'profile'):  # Ensure the Profile exists
            instance.profile.save()
    except Exception as e:
        # Log or handle exceptions for debugging
        print(f"Error saving Profile for User {instance}: {e}")

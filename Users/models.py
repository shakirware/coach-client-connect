from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_coach = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='client_profile_images/', blank=True, null=True)

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coachprofile')
    full_name = models.CharField(max_length=255, null=True, blank=True)
    qualifications = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)  
    specializations = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='coach_profile_images/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    rates = models.CharField(max_length=255, blank=True, null=True)
    languages = models.CharField(max_length=255, blank=True, null=True)
    availability = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    awards = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Coach Profile"
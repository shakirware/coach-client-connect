from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_coach = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='coachprofile')
    qualifications = models.TextField()
    experience = models.TextField()  
    specializations = models.TextField()


    def __str__(self):
        return f"{self.user.username}'s Coach Profile"
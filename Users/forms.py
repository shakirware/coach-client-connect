from django.contrib.auth.forms import UserCreationForm

from django import forms

from .models import User, Coach

class CustomUserCreationForm(UserCreationForm):
    is_coach = forms.BooleanField(required=False, label="Are you a coach?")
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'is_coach') 
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_coach = self.cleaned_data.get("is_coach")

        if commit:
            user.save()
            if user.is_coach:
                # Create an empty CoachProfile for the new coach user
                Coach.objects.create(user=user)

        return user

class CoachProfileForm(forms.ModelForm):
    class Meta:
        model = Coach
        fields = [
            'full_name',
            'qualifications',
            'experience',
            'specializations',
            'profile_picture',
            'bio',
            'rates',
            'languages',
            'availability',
            'location',
            'awards'
        ]
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['bio', 'profile_picture']
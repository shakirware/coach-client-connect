from django.urls import reverse_lazy

from django.views.generic import TemplateView, CreateView, UpdateView

from django.views.generic.edit import DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model

from .forms import CustomUserCreationForm, CoachProfileForm, UserProfileForm

from .models import Coach

User = get_user_model()

class SignUpView(CreateView):
    template_name='signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    
    
class HomeView(TemplateView):
    template_name='home.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'profile.html'  # Specify the template name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = kwargs['username']  # Get the username from the URL parameter
        user_profile = User.objects.get(username=username)  # Fetch the user's profile
        context['user_profile'] = user_profile  # Add the user profile to the context
        return context
        
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm  
    template_name = 'profile_edit.html'
    
    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})
    
    def get_object(self, queryset=None):
        return self.request.user

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'account_delete_confirm.html'
    success_url = reverse_lazy('home')  # Redirect to home page after deletion

    def get_object(self):
        return self.request.user    

class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.is_coach:
            return ['coach_dashboard.html']
        else:
            return ['client_dashboard.html']
    

class CoachProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'coach_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.request.user.coachprofile
        context['coach_profile'] = user_profile
        return context

class CoachProfileEditView(LoginRequiredMixin, UpdateView):
    model = Coach
    form_class = CoachProfileForm
    template_name = 'coach_profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('coach_profile')

    def get_object(self, queryset=None):
        return self.request.user.coachprofile
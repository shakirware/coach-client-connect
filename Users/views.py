from django.urls import reverse_lazy

from django.views.generic import TemplateView, CreateView, UpdateView

from django.views.generic.edit import DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth import get_user_model

from django.shortcuts import get_object_or_404

from .forms import CustomUserCreationForm, CoachProfileForm, UserProfileForm

from .models import Coach

from Messaging.models import Conversation

from Reviews.models import Review

from Reviews.forms import ReviewForm

from django.db.models import Max

User = get_user_model()

class SignUpView(CreateView):
    template_name='Users/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    
    
class HomeView(TemplateView):
    template_name='Users/home.html'

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'Users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = kwargs['username']
        user_profile = get_object_or_404(User, username=username)
        context['user_profile'] = user_profile
        return context
        
class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'Users/profile_edit.html'

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'username': self.request.user.username})

    def get_object(self, queryset=None):
        username = self.kwargs['username']
        return get_object_or_404(User, username=username)

class DeleteAccountView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'Users/account_delete_confirm.html'
    success_url = reverse_lazy('home')  # Redirect to home page after deletion

    def get_object(self):
        return self.request.user    

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'Users/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Retrieve conversations for the current user
        conversations = user.conversations.all()

        # Create a list to store the last message for each conversation
        last_messages = []

        for conversation in conversations:
            last_message = conversation.messages.order_by('-timestamp').first()
            last_messages.append(last_message)

        context['conversations_and_messages'] = zip(conversations, last_messages)
        return context

class CoachProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'Users/coach_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=kwargs['username'])
        coach = user.coachprofile

        # Fetch reviews for this coach
        reviews = Review.objects.filter(coach=coach)
        context['coach_profile'] = coach
        context['reviews'] = reviews
        context['review_form'] = ReviewForm() 

        return context

class CoachProfileEditView(LoginRequiredMixin, UpdateView):
    model = Coach
    form_class = CoachProfileForm
    template_name = 'Users/coach_profile_edit.html'

    def get_success_url(self):
        # Redirect back to the same coach's profile page
        return reverse_lazy('coach_profile', kwargs={'username': self.request.user.username})

    def get_object(self, queryset=None):
        # Fetch the user based on the username in the URL
        user = get_object_or_404(User, username=self.kwargs['username'])
        return user.coachprofile
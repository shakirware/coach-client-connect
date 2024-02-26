from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView
from .models import Review, Coach
from Users.models import User
from .forms import ReviewForm

class AddReviewView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'Reviews/add_review.html'

    def form_valid(self, form):
        # Fetch the Coach instance based on the User's username
        coach_user = get_object_or_404(User, username=self.kwargs['username'])
        coach = get_object_or_404(Coach, user=coach_user)

        form.instance.coach = coach
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect to the coach profile using username
        return reverse('coach_profile', kwargs={'username': self.kwargs['username']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        coach_user = get_object_or_404(User, username=self.kwargs['username'])
        context['coach'] = get_object_or_404(Coach, user=coach_user)
        return context

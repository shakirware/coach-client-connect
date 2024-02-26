from django.urls import path
from .views import CoachListView

urlpatterns = [
    path('coach/', CoachListView.as_view(), name='coach_list'),
]

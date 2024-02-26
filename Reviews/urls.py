from django.urls import path
from .views import AddReviewView

urlpatterns = [
    # ... other patterns ...
    path('coach/<str:username>/add_review/', AddReviewView.as_view(), name='add_review'),
]

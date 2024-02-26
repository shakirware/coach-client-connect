from .views import *

from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView

from django.conf.urls.static import static  

from django.conf import settings

urlpatterns = [
    path('login/', LoginView.as_view(template_name='Users/login.html'), name='login'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('password_change/', PasswordChangeView.as_view(template_name='Users/password_change_form.html'), name='password_change'),
    
    path('password_change/done/', PasswordChangeDoneView.as_view(template_name='Users/password_change_done.html'), name='password_change_done'),

    path('', HomeView.as_view(), name='home'),
    
    path('signup/', SignUpView.as_view(), name='signup'),
    
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    
    path('profile/<str:username>/edit', ProfileEditView.as_view(), name='profile_edit'),
    
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    
    path('coach/profile/<str:username>/', CoachProfileView.as_view(), name='coach_profile'),
    
    path('coach/profile/<str:username>/edit', CoachProfileEditView.as_view(), name='edit_coach_profile'),
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
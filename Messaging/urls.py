from django.urls import path
from .views import *

urlpatterns = [
    # URL pattern for sending a message within a conversation
    path('conversations/<str:conversation_id>/send/', SendMessageView.as_view(), name='send_message'),

    
    # URL pattern for starting a conversation with a coach
    path('start_conversation/<str:username>/', StartConversationView.as_view(), name='start_conversation'),
    
    path('delete_conversation/<str:conversation_id>/', DeleteConversationView.as_view(), name='delete_conversation'),
]

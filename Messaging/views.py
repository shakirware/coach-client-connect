import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin  
from .models import Message, Conversation, Participant
from .forms import MessageForm
from Users.models import User
from django.urls import reverse

from .pusher import pusher_client

class SendMessageView(LoginRequiredMixin, View):
    template_name = 'Messaging/send_message.html'

    def get(self, request, conversation_id):
        # Get the conversation if the user is a participant (either sender or receiver)
        conversation = get_object_or_404(Conversation, participants=request.user, pk=conversation_id)
        form = MessageForm()

        return render(request, self.template_name, {'conversation': conversation, 'form': form})

    def post(self, request, conversation_id):
        # Get the conversation if the user is a participant (either sender or receiver)
        conversation = get_object_or_404(Conversation, participants=request.user, pk=conversation_id)
        form = MessageForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data['content']
            message = Message(conversation=conversation, sender=request.user, content=content)
            message.save()

            formatted_timestamp = message.timestamp.strftime('%b. %d, %Y, %I:%M %p')
        
            # Trigger an event to Pusher
            pusher_client.trigger(
                f'conversation_{conversation_id}',  # Unique channel for each conversation
                'new_message',  # Event name
                {'message': content, 'sender': request.user.username, 'timestamp': formatted_timestamp}
            )

            return redirect('send_message', conversation_id=conversation.id)

        return render(request, self.template_name, {'conversation': conversation, 'form': form})


class StartConversationView(LoginRequiredMixin, View):
    def post(self, request, username):
        user = get_object_or_404(User, username=username)

        # Check if a conversation already exists between the users
        conversation = Conversation.objects.filter(participants=request.user).filter(participants=user).first()

        if conversation:
            # If the conversation exists but is marked as deleted, undelete it
            participant = Participant.objects.get(conversation=conversation, user=request.user)
            if participant.has_deleted:
                participant.has_deleted = False
                participant.save()
        else:
            # If the conversation doesn't exist, create a new conversation
            conversation_id = uuid.uuid4()
            conversation = Conversation.objects.create(id=str(conversation_id))
            conversation.participants.add(request.user, user)

        return redirect('send_message', conversation_id=conversation.id)



class DeleteConversationView(LoginRequiredMixin, View):
    def post(self, request, conversation_id):
        # Get the conversation if the user is a participant (either sender or receiver)
        conversation = get_object_or_404(Conversation, participants=request.user, pk=conversation_id)

        # Mark the participant as deleted
        try:
            participant = Participant.objects.get(conversation=conversation, user=request.user)
            participant.has_deleted = True
            participant.save()

            # Check if both participants have marked the conversation as deleted
            participants = conversation.participants.all()
            if participants.filter(participant__has_deleted=False).count() == 0:
                conversation.delete()


        except Participant.DoesNotExist:
            # Handle the case where the participant does not exist
            pass

        return redirect('dashboard')


import uuid
from django.db import models
from Users.models import User


class Conversation(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    participants = models.ManyToManyField(User, related_name='conversations', through='Participant')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"

class Participant(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    has_deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('conversation', 'user')

    def __str__(self):
        return f"Participant {self.user} in Conversation {self.conversation.id}"



class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender} to Conversation {self.conversation.id}"

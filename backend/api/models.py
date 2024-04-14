from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    startedat = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='conversations', on_delete=models.CASCADE)

    def __str__(self):
        return f"Conversation {self.id} started at {self.start_time}"

class Message(models.Model):
  conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages")
  text = models.TextField()
  sender_type = models.CharField(max_length=10, choices=(('user', 'User'), ('ai', 'AI')))
  createdat = models.DateTimeField(auto_now_add=True)
  updatedat = models.DateTimeField(auto_now=True)

  def __str__(self):
      return f"Message from {self.sender_type} at {self.createdat}: {self.text}"

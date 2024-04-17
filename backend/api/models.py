from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    startedat = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='conversations', on_delete=models.CASCADE)

    def __str__(self):
        return f"Conversation {self.id} started at {self.startedat}"

# Todo: Remove nulls=True after testing
class Message(models.Model):
  conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="messages", null=True)
  text = models.TextField(null=True)
  audio_file = models.FileField(upload_to='messages_audios/', null=True, blank=True)
  sender_type = models.CharField(max_length=10, null=True, choices=(('user', 'User'), ('ai', 'AI')))
  createdat = models.DateTimeField(auto_now_add=True, null=True)
  updatedat = models.DateTimeField(auto_now=True, null=True)

  def __str__(self):
      return f"Message from {self.user} at {self.createdat}: {self.text}"

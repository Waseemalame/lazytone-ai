from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Message, Conversation

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ["id", "username", "password"]
    extra_kwargs = {"password": {"write_only": True}}

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user

class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Message
    fields = ["id", "conversation", "user", "sender_type", "text", "createdat", "updatedat"]
    extra_kwards = {"user": {"read_only": True}}

class ConversationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Conversation
    fields = ["id", "user", "text", "createdat", "updatedat"]
    extra_kwards = {"user": {"read_only": True}}

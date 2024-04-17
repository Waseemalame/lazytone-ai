from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import generics, status
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
import os
import requests
from .models import Message, Conversation

# Conversations
class ConversationListCreate(generics.ListCreateAPIView):
  serializer_class = ConversationSerializer
  permission_classes = [IsAuthenticated]

  def get_queryset(self):
    return Conversation.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    # The post method will validate the serializer before this function is called
    serializer.save(user=self.request.user)

class ConversationDelete(generics.DestroyAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # This will ensure that a user can only access their own conversations
        return Conversation.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        conversation = get_object_or_404(Conversation, id=kwargs['id'], user=request.user)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#  Messages
class MessageListCreate(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(user=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)


class CreateUserView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = [AllowAny]

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

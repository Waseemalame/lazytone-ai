from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.http import FileResponse
from rest_framework import generics, status
from .serializers import UserSerializer, MessageSerializer, ConversationSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from decouple import config
import openai
import tempfile
import os
import requests
from .models import Message, Conversation
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt

openai_api_key = config('OPENAI_API_KEY')
openai.api_key = openai_api_key

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

    def delete(self, request, *args, **kwargs):
        conversation = get_object_or_404(Message, id=kwargs['id'], user=request.user)
        conversation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OpenAIAudioAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'chatbot.html')

    def post(self, request, *args, **kwargs):
        message = request.data.get('message')
        print("Received message:", message)  # Debugging statement
        response = self._ask_openai(message)
        print("Generated response:", response)  # Debugging statement

        # Save AI response
        self._save_message(response['content'], request.user, sender_type='ai')

        return Response({
            'message': message,
            'response': response['content']
        })

    def _ask_openai(self, message):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0125",  # Updated model name for clarity that it's a chat model
            messages=[{"role": "user", "content": message}],
            max_tokens=150,
            temperature=0.7
        )
        print(response)
        answer = response['choices'][0]['message']['content'].strip()  # Updated path for chat completions
        return {'content': answer}

    def _save_message(self, text, user, sender_type):
        data = {'text': text, 'user': user.id, 'sender_type': sender_type}
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)
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

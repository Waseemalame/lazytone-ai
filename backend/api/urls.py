from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.ConversationListCreate.as_view(), name='conversation-list-create'),
    path('conversations/<int:pk>/', views.ConversationDelete.as_view(), name='conversation-delete'),
    path('conversations/<int:conversation_id>/messages/', views.MessageListCreate.as_view(), name='message-list-create'),
    path('messages/', views.MessageListCreate.as_view(), name='message-list'),
    path('voicebot/', views.OpenAIAudioAPIView.as_view(), name='message-list'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('conversations/', views.ConversationListCreate.as_view(), name='conversation-list-create'),
    path('conversations/<int:pk>/', views.ConversationDelete.as_view(), name='conversation-delete'),
    path('conversations/<int:conversation_id>/messages/', views.MessageListCreate.as_view(), name='message-list-create'),
    path('conversations/<int:conversation_id>/messages/process/', views.OpenAIResponseView.as_view(), name='openai-process'),
    path('messages/', views.MessageListCreate.as_view(), name='message-list'),
]

from django.urls import path

from .api import viewsets

urlpatterns = [
    path('messages', viewsets.send_message),
    path('messages/<int:chat_id>/', viewsets.get_messages),
    path('group_chat', viewsets.create_group_chat),
    path('group_chat/<int:chat_id>/participants', viewsets.add_participant_to_chat),
    path('group_chat/<int:chat_id>/participants/<int:user_id>', viewsets.delete_participant_from_chat),
]
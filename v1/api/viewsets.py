from rest_framework.views import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import User, Chat, Message, ChatMember
from .serializers import UserSerializer, ChatSerializer, MessageSerializer, ChatMemberSerializer



@api_view(['POST'])
def send_message(request):
    try:
        db_chat = Chat.objects.get(pk=request.data['chat'])
    except Chat.DoesNotExist:
        return Response(create_error('Chat not found!'), status=status.HTTP_400_BAD_REQUEST)
    try:
        db_member = User.objects.get(pk=request.data['sender'])
    except User.DoesNotExist:
        return Response(create_error('User not found!'), status=status.HTTP_400_BAD_REQUEST)
    is_chat_member = check_chat_member(request.data['chat'], request.data['sender'])
    if not is_chat_member:
        return Response(create_error('User is not a chat member!'), status=status.HTTP_400_BAD_REQUEST)
    db_message = Message.objects.create(
        sender=db_member,
        chat=db_chat,
        text=request.data['text']
    )
    message = MessageSerializer(db_message, many=False)
    return JsonResponse(
        message.data,
        safe=False,
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def get_messages(request, chat_id):
    try:
        chat=Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        return Response(create_error('Chat does not exist!'), status=status.HTTP_400_BAD_REQUEST)
    db_messages = Message.objects.filter(chat=chat.id).all()
    messages = MessageSerializer(db_messages, many=True)
    return Response(messages.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_group_chat(request):
    members = request.data['members']
    db_members = []
    if len(members) < 2:
        return Response(create_error('Too less members!'), status=400)
    for user_id in members:
        try:
            db_members.append(User.objects.get(pk=user_id))
        except User.DoesNotExist:
            return Response(create_error('Member: {} does not exist!'.format(user_id)), status=status.HTTP_400_BAD_REQUEST)
    db_chat = Chat.objects.create(
        name=request.data['name'],
        group_chat=True
    )
    for user in db_members:
        member = ChatMember.objects.create(
            user=user,
            chat=db_chat
        )
    chat = ChatSerializer(db_chat, many=False)
    return JsonResponse(
        chat.data,
        safe=False,
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def add_participant_to_chat(request, chat_id):
    try:
        db_chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        return Response(create_error('Chat not found!'), status=status.HTTP_400_BAD_REQUEST)
    try:
        db_member = User.objects.get(pk=request.data['member'])
    except User.DoesNotExist:
        return Response(create_error('User not found!'), status=status.HTTP_400_BAD_REQUEST)
    is_chat_member = check_chat_member(chat_id, request.data['member'])
    if is_chat_member:
        return Response(create_error('User is already a chat member!'), status=status.HTTP_400_BAD_REQUEST)

    db_member = ChatMember.objects.create(
        user=db_member,
        chat=db_chat
    )
    member = ChatMemberSerializer(db_member, many=False)
    return JsonResponse(
        member.data,
        safe=False,
        status=status.HTTP_200_OK
    )

@api_view(['DELETE'])
def delete_participant_from_chat(request, chat_id, user_id):
    try:
        db_chat = Chat.objects.get(pk=chat_id)
    except Chat.DoesNotExist:
        return Response(create_error('Chat not found!'), status=status.HTTP_400_BAD_REQUEST)
    try:
        db_member = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response(create_error('User not found!'), status=status.HTTP_400_BAD_REQUEST)
    is_chat_member = check_chat_member(chat_id, user_id)
    if not is_chat_member:
        return Response(create_error('User is not a chat member!'), status=status.HTTP_400_BAD_REQUEST)

    is_chat_member.delete()
    member = ChatMemberSerializer(is_chat_member, many=False)
    return JsonResponse(
        member.data,
        safe=False,
        status=status.HTTP_200_OK
    )

def check_chat_member(chat_id, user_id):
    try:
        chatMember = ChatMember.objects.get(user=user_id, chat=chat_id)
    except ChatMember.DoesNotExist:
        return False
    return chatMember

def create_error(message):
    error_object = {}
    error_object['message'] = message
    return error_object
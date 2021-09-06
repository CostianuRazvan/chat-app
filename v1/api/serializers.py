from rest_framework import serializers
from django.conf import settings
from ..models import *



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  '__all__'


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields =  '__all__'


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields =  '__all__'


class ChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMember
        fields = '__all__'
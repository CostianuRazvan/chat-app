from django.contrib import admin

# Register your models here.
from .models import User, Chat, Message, ChatMember

admin.site.register(User)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(ChatMember)

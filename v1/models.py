from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    created = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True
    )

    def __str__(self):
        return str(self.id)

class Chat(models.Model):
    name = models.CharField(max_length=200)
    group_chat = models.BooleanField(
        default=False
    )
    created = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True
    )

    def __str__(self):
        return str(self.id)

class ChatMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    created = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True
    )

    def __str__(self):
        return str(self.id)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    created = models.DateTimeField(
        verbose_name="Created",
        auto_now_add=True
    )

    def __str__(self):
        return str(self.id)




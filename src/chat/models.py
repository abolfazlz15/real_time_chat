import random

from django.contrib.auth import get_user_model
from django.db import models


def unique_generator(length=10):
    source = 'abcdefghijklmnopqrztuvwxyz'
    result = ''
    for i in range(length):
        result += source[random.randint(0, length)]
    return result


class GroupChat(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=65)
    unique_code = models.CharField(max_length=10, default=unique_generator)
    date_created = models.DateTimeField(auto_now_add=True)
    

class Member(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Message(models.Model):
    chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField(default="")
    date_created = models.DateTimeField(auto_now_add=True)

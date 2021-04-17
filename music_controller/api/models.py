import string
import random
import uuid
from django.db import models

from functools import partial


def generate_unique_code(length=32):
    while True:
        code = uuid.uuid4().hex[:length]
        if not Room.objects.filter(code=code).exists():
            break
    return code


def get_next_host():
    guests = Guest.objects.all()
    return guests[0]


class User(models.Model):
    code = models.CharField(max_length=32,
                            default=generate_unique_code,
                            primary_key=True)
    name = models.CharField(max_length=32, default="Anonymous")
    nick_name = models.CharField(max_length=32, default="Anon")


class Room(models.Model):
    code = models.CharField(max_length=32,
                            default=generate_unique_code,
                            unique=True,
                            primary_key=True)
    host = models.ForeignKey(User,
                             null=True,
                             unique=False,
                             on_delete=models.SET_NULL,
                             related_name='host')
    guests = models.ManyToManyField(User, related_name='guests')
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.PositiveIntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

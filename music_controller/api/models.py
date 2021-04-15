import string
import random
import uuid
from django.db import models


def generate_unique_code(length=32):
    while True:
        code = uuid.uuid4().hex[:length]
        if not Room.objects.filter(code=code).exists():
            break
    return code


def generate_unique_nickname(room_code, length=8):
    room = Room.objects.filter(code=room_code)
    if room.exists():
        nicknames = Guest.objects.values_list('nick_name', flat=True).filter(room_code=room)
        while True:
            nickname = uuid.uuid4().hex[:length]
            if nickname not in nicknames:
                return nickname
    raise models.ObjectDoesNotExist()


def get_next_host():
    guests = Guest.objects.all()
    return guests[0]


class Host(models.Model):
    nick_name = models.CharField(max_length=32, default="Anon")


class Room(models.Model):
    code = models.CharField(max_length=32, default=generate_unique_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    host_n = models.ForeignKey(Host, null=True, on_delete=models.SET(get_next_host))
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.PositiveIntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)


# Docs look at Restaurant/Place analogy.
# Should a host be allowed to join other rooms as guest?
class Guest(models.Model):
    nick_name = models.CharField(max_length=32, default=generate_unique_nickname)
    room_code = models.ForeignKey(Room, default=None, null=True, on_delete=models.SET_DEFAULT)

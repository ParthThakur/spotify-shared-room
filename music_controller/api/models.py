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


class Room(models.Model):
    code = models.CharField(max_length=32, default='', unique=True)
    host = models.CharField(max_length=50, unique=True)
    guest_can_pause = models.BooleanField(null=False, default=False)
    votes_to_skip = models.PositiveIntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

from rest_framework import serializers
from .models import Room


class RoomSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

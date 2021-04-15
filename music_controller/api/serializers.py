from rest_framework import serializers
from .models import Room, Host


class HostSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = ('nick_name',)


class RoomSerializer(serializers.ModelSerializer):
    host = HostSerialiser(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'host')


class UpdateRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[])

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'code')

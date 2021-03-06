from rest_framework import serializers
from .models import Room, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('code',)


class RoomSerializer(serializers.ModelSerializer):
    guests = GuestSerializer(many=True, read_only=True)
    host = UserSerializer(read_only=True)

    class Meta:
        model = Room
        fields = "__all__"


class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'nick_name')


class UpdateRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[])

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'code')

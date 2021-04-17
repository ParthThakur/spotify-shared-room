from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room, User
from .serializers import RoomSerializer, UserSerializer, CreateRoomSerializer, CreateUserSerializer, UpdateRoomSerializer
import api.responses as responses


def get_or_create_user(request, *args, **kwargs):
    code = request.session.get('user_code')
    try:
        return User.objects.get(code=code)
    except ObjectDoesNotExist:
        user = User(**kwargs)
        user.save()
        request.session['user_code'] = user.code
        return user


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class UserView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwrg = 'code'

    def get(self, request, format=None):
        room_code = request.GET.get(self.lookup_url_kwrg)
        if room_code is not None:
            try:
                room = Room.objects.get(code=room_code)
                user = get_or_create_user(self.request)
                data = self.serializer_class(room).data
                data['is_host'] = room.host == user
                return Response(data, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return responses.ERROR_DOES_NOT_EXIST

        return responses.ERROR_BAD_REQUEST


class CreateRoom(APIView):
    serializer_class = CreateRoomSerializer
    user_serializer = CreateUserSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        try:
            room_data = {key: request.data[key] for key in [
                'guest_can_pause', 'votes_to_skip']}
            user_data = {key: request.data[key]
                         for key in ['name', 'nick_name']}
        except KeyError:
            return responses.ERROR_BAD_REQUEST

        serializer = self.serializer_class(data=room_data)
        serializer_user = self.user_serializer(data=user_data)
        if serializer.is_valid() and serializer_user.is_valid():

            user_nick_name = serializer_user.data.get('nick_name')
            user_name = serializer_user.data.get('name')
            user = get_or_create_user(self.request,
                                      nick_name=user_nick_name,
                                      name=user_name)
            if user.nick_name != user_nick_name:
                user.nick_name = user_nick_name
                user.save(update_fields=['nick_name'])
            if user.name != user_name:
                user.name = user_name
                user.save(update_fields=['name'])

            room_code = self.request.session.get('room_code')
            gcp = serializer.data.get('guest_can_pause')
            vts = serializer.data.get('votes_to_skip')

            if room_code and self.request.session.get('create_new'):
                room = Room.objects.get(code=room_code)
                room.guest_can_pause = gcp
                room.votes_to_skip = vts
                room.save()
            else:
                room = Room(host=user,
                            guest_can_pause=gcp,
                            votes_to_skip=vts)
                room.save()

            room.guests.add(user)
            self.request.session['room_code'] = room.code
            return Response(RoomSerializer(room).data, status=status.HTTP_202_ACCEPTED)

        return responses.ERROR_BAD_REQUEST


class JoinRoom(APIView):
    lookup_url_kwrg = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        room_code = request.data.get(self.lookup_url_kwrg)
        user = get_or_create_user(self.request)

        try:
            room = Room.objects.get(code=room_code)
            room.guests.add(user)
            self.request.session['room_code'] = room.code
            return responses.SUCCESS_JOINED

        except ObjectDoesNotExist:
            return responses.ERROR_DOES_NOT_EXIST

        return responses.ERROR_BAD_REQUEST


class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {
            'code': self.request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    def post(self, request, format=None):

        room_code = request.session.get('room_code')

        try:
            room = Room.objects.get(code=room_code)
            user = get_or_create_user(self.request)
            room.guests.remove(user)
            self.request.session.pop('room_code')
            return responses.SUCCESS_LEFT

        except ObjectDoesNotExist:
            self.request.session.pop('room_code')

        return responses.ERROR_NOT_IN_ROOM


class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer
    user_serializer = CreateUserSerializer

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        try:
            room_data = {key: request.data[key] for key in [
                'guest_can_pause', 'votes_to_skip', 'code']}
            user_data = {key: request.data[key]
                         for key in ['name', 'nick_name']}
        except KeyError:
            return responses.ERROR_BAD_REQUEST

        serializer = self.serializer_class(data=room_data)
        serializer_user = self.user_serializer(data=user_data)
        if serializer.is_valid() and serializer_user.is_valid():

            user_new_nick_name = serializer_user.data.get('nick_name')
            user_new_name = serializer_user.data.get('name')
            try:
                user = User.objects.get(code=request.session.get('user_code'))
                if user.nick_name != user_new_nick_name:
                    user.nick_name = user_new_nick_name
                    user.save(update_fields=['nick_name'])
                if user.name != user_new_name:
                    user.name = user_new_name
                    user.save(update_fields=['name'])

            except ObjectDoesNotExist:
                return responses.ERROR_USER_DOES_NOT_EXIST

            room_code = serializer.data.get('code')
            try:
                room = Room.objects.get(code=room_code)
                if room.host == user:
                    room.guest_can_pause = serializer.data.get(
                        'guest_can_pause')
                    room.votes_to_skip = serializer.data.get('votes_to_skip')
                    room.save(update_fields=['guest_can_pause',
                                             'votes_to_skip'])

                    return responses.SUCCESS_UPDATED

                return responses.ERROR_NOT_A_HOST

            except ObjectDoesNotExist:
                return responses.ERROR_DOES_NOT_EXIST

        return responses.ERROR_BAD_REQUEST

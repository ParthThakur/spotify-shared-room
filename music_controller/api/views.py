from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room, User
from .serializers import RoomSerializer, UserSerializer, CreateRoomSerializer, CreateUserSerializer, UpdateRoomSerializer
import api.responses as responses


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwrg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwrg)
        if code is not None:
            try:
                room = Room.objects.get(code=code)
                data = self.serializer_class(room).data
                data['is_host'] = self.request.session.get('user_code') == room.host
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
            room_data = {key: request.data[key] for key in ['guest_can_pause', 'votes_to_skip']}
            user_data = {key: request.data[key] for key in ['name', 'nick_name']}
        except KeyError:
            return responses.ERROR_BAD_REQUEST

        serializer = self.serializer_class(data=room_data)
        serializer_user = self.user_serializer(data=user_data)
        if serializer.is_valid() and serializer_user.is_valid():
            
            user_new_nick_name = serializer_user.data.get('nick_name')
            try:
                user = User.objects.get(code=request.session.get('user_code'))
                if user.nick_name != user_new_nick_name:
                    user.nick_name = user_new_nick_name
                    user.save(update_fields=['nick_name'])

            except ObjectDoesNotExist:
                user = User(nick_name=user_new_nick_name)
                user.save()
                self.request.session['user_code'] = user.code

            room_code = self.request.session.get('room_code')
            gcp = serializer.data.get('guest_can_pause')
            vts = serializer.data.get('votes_to_skip')
            
            if room_code and self.request.session.get('create_new'):
                room = Room.objects.get(code=room_code)
                room.guest_can_pause = gcp
                room.votes_to_skip = vts
                room.save()
            else:
                room = Room(host=user.code,
                            guest_can_pause=gcp,
                            votes_to_skip=vts)
                room.save()
            
            user.rooms.add(room)
            self.request.session['room_code'] = room.code
            return Response(RoomSerializer(room).data, status=status.HTTP_202_ACCEPTED)

        return responses.ERROR_BAD_REQUEST


class JoinRoom(APIView):
    lookup_url_kwrg = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        room_code = request.data.get(self.lookup_url_kwrg)
        user_code = request.session.get('user_code')
        if user_code:
            user = User.objects.get(code=user_code)
        else:
            user = User()
            user.save()

        try:
            room = Room.objects.get(code=room_code)
            self.request.session['room_code'] = room.code
            user.rooms.add(room)
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
        user_code = request.session.get('user_code')

        try:
            room = Room.objects.get(code=room_code)
            user = User.objects.get(code=user_code, rooms=room)
            user.rooms.remove(room)
            self.request.session.pop('room_code')
            return responses.SUCCESS_LEFT

        except ObjectDoesNotExist:
            self.request.session.pop('room_code')
            return responses.ERROR_NOT_IN_ROOM

        return responses.ERROR_NOT_IN_ROOM


class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            room_code = serializer.data.get('code')
            queryset = Room.objects.filter(code=room_code)
            if queryset.exists():
                room = queryset[0]                
                user_id = self.request.session.session_key
                if room.host == user_id:
                    room.guest_can_pause = serializer.data.get('guest_can_pause')
                    room.votes_to_skip = serializer.data.get('votes_to_skip')
                    room.save(update_fields=['guest_can_pause', 'votes_to_skip'])

                    return responses.SUCCESS_UPDATED
                
                return responses.ERROR_NOT_A_HOST

            return responses.ERROR_DOES_NOT_EXIST       
        
        return responses.ERROR_BAD_REQUEST


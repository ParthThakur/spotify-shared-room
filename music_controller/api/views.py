from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room, User
from .serializers import RoomSerializer, UserSerializer, CreateRoomSerializer, CreateUserSerializer, UpdateRoomSerializer
import api.responses as responses

import sys


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwrg = 'code'

    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwrg)
        if code is not None:
            room = Room.objects.filter(code=code)
            if room.exists():
                data = self.serializer_class(room[0]).data
                data['is_host'] = self.request.session['host_code'] == room[0].host.id
                return Response(data, status=status.HTTP_200_OK)
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
            host_data = {key: request.data[key] for key in ['nick_name']}
        except KeyError:
            return responses.ERROR_BAD_REQUEST

        serializer = self.serializer_class(data=room_data)
        serializer_host = self.host_serialiser(data=host_data)
        if serializer.is_valid() and serializer_host.is_valid():
            
            host = Host.objects.filter(id=request.session['code'])
            host_nick_name = serializer_host.data.get('nick_name')
            if host.exists():
                host = host[0]
                if host.nick_name != host_nick_name:
                    host.nick_name = host_nick_name
                    host.save(update_fields=['nick_name'])
            else:
                host = Host(nick_name=host_nick_name)
                host.save()
                self.request.session['code'] = host.id

            queryset = Room.objects.filter(host=host)
            gcp = serializer.data.get('guest_can_pause')
            vts = serializer.data.get('votes_to_skip')

            if queryset.exists() and request.data['update']:
                room = queryset[0]
                room.guest_can_pause = gcp
                room.votes_to_skip = vts
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])

            else:
                user = User(nick_name=user_nick_name)
                user.save()
                self.request.session['user_code'] = user.code

            room = Room(host=user.code,
                        guest_can_pause=serializer.data.get('guest_can_pause'),
                        votes_to_skip=serializer.data.get('votes_to_skip'))
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
        user_code = request.session['code']
        if user_code:
            user = User.objects.get(id=user_code)
        else:
            user = User()
        if room_code is not None:
            queryset = Room.objects.filter(code=room_code)
            if queryset.exists():
                room = queryset[0]
                self.request.session['room_code'] = room_code
                return responses.SUCCESS_JOINED
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
        if 'room_code' in request.session:
            self.request.session.pop('room_code')
            host = Room.objects.filter(host=request.session.session_key)
            if host.exists():
                host[0].delete()
            return responses.SUCCESS_LEFT

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


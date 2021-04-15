from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room, Host
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer, HostSerialiser
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
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return responses.ERROR_DOES_NOT_EXIST

        return responses.ERROR_BAD_REQUEST


class CreateRoom(APIView):
    serializer_class = CreateRoomSerializer
    host_serialiser = HostSerialiser

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
            host = Host(nick_name=serializer_host.data.get('nick_name'))
            host.save()

            queryset = Room.objects.filter(host=host)
            gcp = serializer.data.get('guest_can_pause')
            vts = serializer.data.get('votes_to_skip')

            if queryset.exists() and request.data['update']:
                room = queryset[0]
                room.guest_can_pause = gcp
                room.votes_to_skip = vts
                room.save(update_fields=['guest_can_pause', 'votes_to_skip'])

            else:
                room = Room(host=host,
                            guest_can_pause=gcp,
                            votes_to_skip=vts)
                room.save()

            self.request.session['room_code'] = room.code
            return Response(RoomSerializer(room).data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class JoinRoom(APIView):
    lookup_url_kwrg = 'code'

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get(self.lookup_url_kwrg)
        if code is not None:
            queryset = Room.objects.filter(code=code)
            if queryset.exists():
                room = queryset[0]
                self.request.session['room_code'] = code
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


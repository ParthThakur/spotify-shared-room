from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer


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
            return Response({'Error': 'Room does not exist or invalid code.'}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({'Error': 'Bad request'}, status=status.HTTP_400_BAD_REQUEST)


class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            gcp = serializer.data.get('guest_can_pause')
            vts = serializer.data.get('votes_to_skip')

            if queryset.exists():
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
                return Response({'Success': 'Room joined successfully'}, status=status.HTTP_200_OK)
            return Response({'Error': 'Room not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Error': 'Bad Request'}, status=status.HTTP_400_BAD_REQUEST)


class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
                self.request.session.create()
        
        data = {
            'code': self.request.session.get('room_code')
        }
        return JsonResponse(data, status=status.HTTP_200_OK)

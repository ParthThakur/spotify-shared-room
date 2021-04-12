from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room
from .serializers import RoomSerializer, CreateRoomSerializer


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


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

            return Response(RoomSerializer(room).data, status=status.HTTP_202_ACCEPTED)
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


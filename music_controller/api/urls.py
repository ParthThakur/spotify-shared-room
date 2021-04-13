from django.urls import path
from .views import RoomView, CreateRoomView, GetRoom, JoinRoom


urlpatterns = [
    path('room', RoomView.as_view()),
    path('createRoom', CreateRoomView.as_view()),
    path('getRoom', GetRoom.as_view()),
    path('joinRoom', JoinRoom.as_view()),
]
from django.urls import path
from .views import RoomView, UserView, CreateRoom, GetRoom, JoinRoom, UserInRoom, LeaveRoom, UpdateRoom


urlpatterns = [
    path('rooms', RoomView.as_view()),
    path('users', UserView.as_view()),
    path('createRoom', CreateRoom.as_view()),
    path('getRoom', GetRoom.as_view()),
    path('joinRoom', JoinRoom.as_view()),
    path('userInRoom', UserInRoom.as_view()),
    path('leaveRoom', LeaveRoom.as_view()),
    path('updateRoom', UpdateRoom.as_view()),
]

from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('room/<str:roomCode>', index),
    path('<str:page>', index),
]

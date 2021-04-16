from django.urls import path
from .views import AuthURL

urlpatterns = [
    path('getAuthURL', AuthURL)
]

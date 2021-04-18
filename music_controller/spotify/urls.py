from django.urls import path
from .views import AuthURL, spotify_callback, IsSpotifyAuthenticated, CurrentSong

urlpatterns = [
    path('getAuthURL', AuthURL.as_view()),
    path('redirect', spotify_callback),
    path('isAuthenticated', IsSpotifyAuthenticated.as_view()),
    path('getCurrentSong', CurrentSong.as_view())
]

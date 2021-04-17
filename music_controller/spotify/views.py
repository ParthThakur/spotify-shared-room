from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post

from .secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from .utils import update_or_create_user_tokens, is_spotify_authenticated
from .utils import SPOTIFY_URL


class AuthURL(APIView):
    def get(self, request, format=None):
        room = self.request.session['room_code']
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        url = Request('GET', f'{SPOTIFY_URL}/authorize',
                      params={
                          'scope': scopes,
                          'response_type': 'code',
                          'redirect_uri': REDIRECT_URI,
                          'client_id': CLIENT_ID
                      }).prepare().url

        return Response({'url': url}, status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post(f'{SPOTIFY_URL}/api/token',
                    data={
                        'grant_type': 'authorization_code',
                        'code': code,
                        'redirect_uri': REDIRECT_URI,
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET
                    }).json()

    if not request.session.exists(request.session.session_key):
        request.session.create()
    update_or_create_user_tokens(request.session.session_key, **response)
    return redirect(f'frontend:current_room', roomCode=request.session.get('room_code'))


class IsSpotifyAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)

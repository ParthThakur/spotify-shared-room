from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post
from .secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

SPOTIFY_URL = 'https://accounts.spotify.com'


class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'spotify-read-playback user-modify-playback-state user-read-currently-playing'
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

    access_token = response.get('access_token')

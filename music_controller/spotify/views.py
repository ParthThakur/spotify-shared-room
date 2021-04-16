from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post
from .secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

AUTH_URL = 'https://accounts.spotify.com/authorize'


class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'spotify-read-playback user-modify-playback-state user-read-currently-playing'
        url = Request('GET', AUTH_URL, 
                      params={
                          'scope': scopes,
                          'response_type': 'code',
                          'redirect_uri': REDIRECT_URI,
                          'client_id': CLIENT_ID
                      }).prepare().url
        
        return Response({'url': url}, status.HTTP_200_OK)

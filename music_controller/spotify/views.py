from django.shortcuts import render, redirect
from django.db.models import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post

from .secrets import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from .utils import update_or_create_user_tokens, is_spotify_authenticated, make_spotify_api_request, get_song_details, pause_song, play_song
from .utils import SPOTIFY_URL
from api.models import Room
from api.responses import ERROR_DOES_NOT_EXIST, ERROR_NOT_ALLOWED


class AuthURL(APIView):
    def get(self, request, format=None):
        room = self.request.session['room_code']
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'
        url = Request('GET', f'{SPOTIFY_URL}authorize',
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

    response = post(f'{SPOTIFY_URL}api/token',
                    data={
                        'grant_type': 'authorization_code',
                        'code': code,
                        'redirect_uri': REDIRECT_URI,
                        'client_id': CLIENT_ID,
                        'client_secret': CLIENT_SECRET
                    }).json()

    update_or_create_user_tokens(request.session['user_code'], **response)
    return redirect(f'frontend:current_room', roomCode=request.session.get('room_code'))


class IsSpotifyAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session['user_code'])
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


class CurrentSong(APIView):
    def get(self, request, format=None):
        room_code = self.request.session.get('room_code')

        try:
            room = Room.objects.get(code=room_code)
            host = room.host
        except ObjectDoesNotExist:
            return ERROR_DOES_NOT_EXIST

        endpoint = 'player/currently-playing'
        response = make_spotify_api_request(host.code, endpoint)

        if 'item' not in response:
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        song = get_song_details(response)

        return Response(song, status=status.HTTP_200_OK)


class PauseSong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')

        try:
            room = Room.objects.get(code=room_code)
            host = room.host
        except ObjectDoesNotExist:
            return ERROR_DOES_NOT_EXIST

        if self.request.session['user_code'] == host.code or room.guest_can_pause:
            pause_song(host.code)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return ERROR_NOT_ALLOWED


class PlaySong(APIView):
    def put(self, response, format=None):
        room_code = self.request.session.get('room_code')

        try:
            room = Room.objects.get(code=room_code)
            host = room.host
        except ObjectDoesNotExist:
            return ERROR_DOES_NOT_EXIST

        if self.request.session['user_code'] == host.code or room.guest_can_pause:
            play_song(host.code)
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        return ERROR_NOT_ALLOWED

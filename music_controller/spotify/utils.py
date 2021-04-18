from .models import SpotifyToken
from .secrets import CLIENT_SECRET, CLIENT_ID
from django.db.models import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta
from requests import post, put, get

SPOTIFY_URL = 'https://accounts.spotify.com/'
BASE_URL = 'https://api.spotify.com/v1/me/'


def get_user_tokens(session_id):
    try:
        return SpotifyToken.objects.get(user=session_id)
    except ObjectDoesNotExist:
        return None


def update_or_create_user_tokens(session_id, **kwargs):
    tokens = get_user_tokens(session_id)

    if tokens:
        expires_in = timezone.now() + timezone.timedelta(seconds=kwargs.get('expires_in'))

        tokens.expires_in = expires_in
        tokens.access_token = kwargs.get('access_token')
        tokens.token_type = kwargs.get('token_type')
        tokens.save(update_fields=['expires_in',
                                   'access_token',
                                   'token_type'])
    else:
        kwargs['expires_in'] = timezone.timedelta(
            seconds=kwargs['expires_in']) + timezone.now()
        tokens = SpotifyToken(
            user=session_id, **{key: kwargs[key] for key in kwargs})
        tokens.save()


def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            try:
                refresh_spotify_token(session_id, tokens)
            except TypeError:
                return False

        return True

    return False


def refresh_spotify_token(session_id, tokens):
    response = post(f'{SPOTIFY_URL}api/token', data={
        'grant_type': 'refesh_token',
        'refresh_token': tokens.refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    if 'error' in response:
        raise TypeError(response)

    update_or_create_user_tokens(
        session_id, **{key: response[key] for key in response})


def make_spotify_api_request(session_id, endpoint, post_=False, put_=False):
    tokens = get_user_tokens(session_id)
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer ' + tokens.access_token}

    if post:
        post(BASE_URL + endpoint, headers=headers)

    if put:
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)

    try:
        return response.json()
    except Exception as e:
        return {'Error': 'Could not make request', 'error_description': str(e), 'spotify_status': response.status_code}


def get_song_details(response):

    item = response.get('item')
    duration = item.get('duration_ms')
    progress = response.get('progress_ms')
    album_cover = item.get('album').get('images')[0].get('url')
    is_playing = response.get('is_playing')
    song_id = item.get('id')

    artist_string = ""

    for i, artist in enumerate(item.get('artists')):
        if i > 0:
            artist_string += ", "
        name = artist.get('name')
        artist_string += name

    song = {
        'title': item.get('name'),
        'artist': artist_string,
        'duration': duration,
        'time': progress,
        'image_url': album_cover,
        'is_playing': is_playing,
        'votes': 0,
        'id': song_id
    }

    return song


def play_song(host_id):
    return make_spotify_api_request(host_id, 'player/play', put_=True)


def pause_song(host_id):
    return make_spotify_api_request(host_id, 'player/pause', put_=True)


def skip_song(host_id):
    return make_spotify_api_request(host_id, 'player/next', post_=True)

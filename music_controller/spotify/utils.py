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
        tokens.refresh_token = kwargs.get('refresh_token')
        tokens.token_type = kwargs.get('token_type')
        tokens.save(update_fields=['expires_in',
                                   'access_token',
                                   'refresh_token',
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


def make_spotify_api_request(session_id, endpoint, post=False, put=False):
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

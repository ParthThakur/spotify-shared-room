from .models import SpotifyToken
from django.db.models import ObjectDoesNotExist
from django.utils import timezone
from datetime import timedelta


def get_user_tokens(session_id):
    try:
        return SpotifyToken.objects.get(user=session_id)
    except ObjectDoesNotExist:
        return None


def update_or_create_user_tokens(session_id, **kwargs):
    tokens = get_user_tokens(session_id)

    if tokens:
        expires_in = timezone.now() + timezone(seconds=kwargs.get('expires_in'))

        tokens.expires_in = expires_in
        tokens.access_token = kwargs.get('access_token')
        tokens.refresh_token = kwargs.get('refresh_token')
        tokens.token_type = kwargs.get('token_type')
        tokens.save(update_fields=['expires_in',
                                   'access_token',
                                   'refresh_token',
                                   'token_type'])
    else:
        tokens = SpotifyToken(
            user=session_id, **{key: kwargs[key] for key in kwargs})
        tokens.save()

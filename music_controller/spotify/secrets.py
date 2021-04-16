from os import environ

CLIENT_ID = environ['SPOTIFY_CLIENT_ID']
CLIENT_SECRET = environ['SPOTIFY_CLIENT_SECRET']
REDIRECT_URI = ""

assert(len(CLIENT_ID) >= 32)
assert(len(CLIENT_SECRET) >= 32)

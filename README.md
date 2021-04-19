# House Party

A shared spotify room created by following [TechWithTim's](https://github.com/techwithtim) React with Django tutorials.
The tutorials can be found [here](https://www.youtube.com/playlist?list=PLzMcBGfZo4-kCLWnGmK0jUBmGLaJxvi4j).

This app lets users host a shared room, which others can join to control the host's spotify playback.

# Installation

#### Pre-requisites:

    Python 3.6 (or above)
    Node.js 14.15

#### Install python libraries:

```bash
   pip install requirements.txt
```

#### Install required NodeJS packages:

##### In the `frontend` folder:

```bash
    npm install
```

#### Compile frontend:

##### For production build:

```bash
    npm run build
```

##### For development build:

```bash
    npm run dev
```

# Start Server

For spotify to connect properly, the api keys need to be present as environment variables. Get them from [spotify developer console.](https://developer.spotify.com/dashboard)

```bash
    SET SPOTIFY_CLIENT_ID=your_client_id
    SET SPOTIFY_CLIENT_SECRET=your_client_secret
```

#### Run django server

##### In the `music_controller` folder:

```bash
    django manage.py runserver
```

# Contrubuting

Forks and pull requests are welcome. Please open an issue if you want to change something major.

The `settings.json` for VS Code is included in the repo to JS and python linters and autoformaters.

# License

[MIT](LICENSE)

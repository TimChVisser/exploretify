# Exploretify
Exploretify is an exploration of the Spotify API intended to assist in the analysis and curation of playlists.

## Getting Started
In order to run main.py, a *client_id* and *client_secret* are required. These can be obtained by creating an application from within Spotify's developer dashboard. These variables must be passed as environment variables as follows:

`SPOTIPY_CLIENT_ID=<client_id>`  
`SPOTIPY_CLIENT_SECRET=<client_secret>`

In addition, a redirect URI must be provided. This only needs to be a valid URI, e.g.:

`SPOTIPY_REDIRECT_URL=http://localhost:80/callback`

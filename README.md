# spotify2tidal
Tool for migrating Spotify playlists to Tidal

Requirements:
* Python 2.x with the requests package installed
* Spotfy and Tidal access tokens (instructions below)

Setup:
* Log in to https://open.spotify.com
* Open your browser's Developer Tools, usually under "More Tools" in the dropdown menu, or  Option + ⌘ + J (on macOS), or Shift + CTRL + J (on Windows/Linux).
* Paste the following into the console:

`var x = document.getElementById("config").innerHTML;console.log(JSON.parse(x)["accessToken"])`
* Save the returned value in a file called `spotify.token` in the same folder as the `spotify2tidal.py` file
* Log in to https://listen.tidal.com/
* Open Developer Tools again and paste the following into the console:

`var x = localStorage.getItem("_TIDAL_activeSession2");console.log(JSON.parse(x)["oAuthAccessToken"])`
* Save the returned value in a file called `tidal.token` in the same folder as the `spotify2tidal.py` file

How to use:

Simply run the `spotify2tidal.py`file like the following:

`python2 spotify2tidal.py`

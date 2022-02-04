# spotify2tidal
Hacky tool for migrating Spotify playlists to Tidal. No guarantee that it will work 100%, but it seems to do the job. Use at your own risk.

Requirements:
* Python 2.x with the requests package installed
* Spotify and Tidal access tokens (instructions below)

Setup:
* Log in to https://open.spotify.com
* Open your browser's Developer Tools, usually under "More Tools" in the dropdown menu, or  Option + ⌘ + J (on macOS), or Shift + CTRL + J (on Windows/Linux).
* Paste the following into the console:

`var x = document.getElementById("config").innerHTML;console.log(JSON.parse(x)["accessToken"])`
* Save the returned value in a file called `spotify.token` in the same folder as the `spotify2tidal.py` file
* Log in to https://listen.tidal.com/
* Open Developer Tools again and paste the following into the console:

`JSON.parse(localStorage.getItem("_TIDAL_activeSession2"))["oAuthAccessToken"]`
* Save the returned value (remove the single quotes) in a file called `tidal.token` in the same folder as the `spotify2tidal.py` file

How to use:

Download the `spotify2tidal.py`file and run it in a terminal like the following:

`python2 spotify2tidal.py`

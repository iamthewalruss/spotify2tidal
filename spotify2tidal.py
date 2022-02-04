#!/usr/bin/python


## this is too deal with the encoding of special characters

import sys
# sys.setdefaultencoding() does not exist, here!
reload(sys)  # Reload does the trick!
sys.setdefaultencoding('UTF8')

import os
import json
import requests


## get spotify token from web browser console:
## var x = document.getElementById("config").innerHTML;console.log(JSON.parse(x)["accessToken"])

spotifyTokenFile = open("spotify.token")
spotifyToken = spotifyTokenFile.readlines()[0].rstrip() ## hacky way of turning the token into a string


## get tidal token:
## JSON.parse(localStorage.getItem("_TIDAL_activeSession2"))["oAuthAccessToken"]

tidalTokenFile = open("tidal.token")
tidalToken = tidalTokenFile.readlines()[0].rstrip() ## hacky way of turning the token into a string



## proxies for debugging
proxies = {
  "http": None,
  "https": None
}



def makeHttpGetSpotify(url):

	## make request and parse result as json
	try:
		r = requests.get(url = url, headers={"Authorization":"Bearer " + spotifyToken,"Accept":"application/json"}) #, proxies=proxies, verify=False)

	except KeyError:
		print "The token has expired"


	data = r.json()

	return data



## parse playlist and output comma-separated list


def parsePlaylist(data):

	## check playlist length
	total = data['total']

	counter = 0

	playlist = ""

	while counter < total:
		## parse artist
		artist = data['items'][counter]['track']['artists'][0]['name']

		## parse title
		title = data['items'][counter]['track']['name']

		## parse album
		album = data['items'][counter]['track']['album']['name']

		## remove commas since this will break the csv formatting
		artist = artist.replace(',', '')
		title = title.replace(',', '')
		album = album.replace(',', '')

		playlist += artist + "," + title + "," + album + "\n"

		## iterate the counter
		counter += 1

	return playlist



def parsePlaylistList(data):

	# check number of playlists
	total = data['length']

	counter = 0

	playlistList = ""

	while counter < total:

		## parse uri
		uri = data['contents']['items'][counter]['uri']
		uri = uri.replace("spotify:playlist:","") ## only keep the playlist identifier

		## parse title
		title = data['contents']['metaItems'][counter]['attributes']['name']

		## check so that we are the owner of the playlist
		if me == data['contents']['metaItems'][counter]['ownerUsername']:
			playlistList += uri + "," + title + "\n"
		else:
			pass

		## iterate the counter
		counter += 1

	return playlistList


def makeHttpGetTidal(url):


	## make request and parse result as json
	try:
		r = requests.get(url = url, headers={"Authorization":"Bearer " + tidalToken,"Accept":"application/json"}, proxies=proxies)

	except KeyError:
		print "The token has expired"


	data = r.json()

	return data



def makeHttpPut(url):


	## make request and parse result as json
	try:
		r = requests.put(url = url, headers={"Authorization":"Bearer " + tidalToken,"Accept":"application/json"}, proxies=proxies)

	except KeyError:
		print "The token has expired"


	data = r.json()

	return data



def makeHttpPost(url, payload):


	## make request and parse result as json
	try:
		r = requests.post(url = url, headers={"Authorization":"Bearer " + tidalToken,"Accept":"application/json","If-None-Match":"*","Content-Type":"application/x-www-form-urlencoded; charset=UTF-8"}, data=payload, proxies=proxies)

	except KeyError:
		print "The token has expired"


	data = r.json()

	return data


def readfiles():
	
	## returns a list of csv files

	files = []
	for file in os.listdir("./"):
		if file.endswith(".csv"):
			files.append(file)

	return files


def makePlaylist(playlistName):

	make_playlist = makeHttpPut("https://api.tidal.com/v2/my-collection/playlists/folders/create-playlist?description=&folderId=root&name=" + playlistName)
	playlist_id = make_playlist["data"]["uuid"]
	print "\n[+] Playlist '" + playlistName + "' created"
	return playlist_id 


def addSongs(playlistId, playlistFile):

	## open the play list file
	f = open(playlistFile).readlines()

	playlist_length = len(f)

	counter = 1

	while playlist_length > counter:
		artist = f[counter].split(",")[0]
		title = f[counter].split(",")[1]

		get_song = makeHttpGetTidal("https://listen.tidal.com/v1/search/top-hits?query=" + artist + "%20" + title.replace("&", "%26") + "&types=ARTISTS,ALBUMS,TRACKS,VIDEOS,PLAYLISTS&countryCode=SE")

		try: 
			if get_song["tracks"]["items"][0]["title"] == title and get_song["tracks"]["items"][0]["artists"][0]["name"] == artist:

				track_id = get_song["tracks"]["items"][0]["id"]

				payload = "onArtifactNotFound=FAIL&onDupes=FAIL&trackIds=" + str(track_id).rstrip()

				add_track = makeHttpPost("https://listen.tidal.com/v1/playlists/" + playlistId + "/items?countryCode=SE", payload)

				counter += 1

				print "[+] Added track " + artist + " - " + title

			else:
				counter += 1
				print "[-] Could not find a direct match for " + artist + " - " + title

		except:
			print "[-] Could not find " + artist + " - " + title

			counter += 1



def spotifyStuff():
	## get a list of user owned playlists 
	playlists = makeHttpGetSpotify("https://spclient.wg.spotify.com/playlist/v2/user/" + me + "/rootlist?decorate=attributes%2Cowner")   

	print "[+] Fetching playlists from Spotify..."

	## parse the response into csv format
	parsedList = parsePlaylistList(playlists)

	## loop over the list to download each playlist

	parsedList = parsedList.split("\n") # make list or the loop will only use the first character of every line

	for x in parsedList:

		## extract the playlist id
		playlistId = x.split(",")[0]

		if playlistId != "":
			playlist = makeHttpGetSpotify("https://api.spotify.com/v1/playlists/" + playlistId + "/tracks?market=from_token")

			title = x.split(",")[1]

			print "[+] Downloading playlist '" + title + "' (" + playlistId + ")"

			## parse the playlist and save as csv
			parsedPlaylist = parsePlaylist(playlist)

			filename = playlistId + ".csv"
			
			f = open(filename, "w")
			f.write(title + "\n" + parsedPlaylist)
			f.close()


def tidalStuff():

	files = readfiles()

	for file in files:
		f = open(file).readlines()
		playlist_name = f[0].rstrip()
		playlistId = makePlaylist(playlist_name)

		print "[+] Adding songs to '" + playlist_name + "'..."
		addSongs(playlistId, file)



def whoami():
	data = makeHttpGetSpotify("https://api.spotify.com/v1/me")
	return data["id"]



def main():
	
	print "[+] Current Spotify user is: " + me + "\n"

	print "[+] Starting Spotify part...\n"
	spotifyStuff()
	print "[+] Spotify part done!\n"

	print "[+] Starting Tidal part..."
	tidalStuff()
	print "[+] Tidal part done!"


## establish user identity
me = whoami()



if __name__ == "__main__":
    main()



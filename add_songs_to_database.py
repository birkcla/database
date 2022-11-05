import sqlite3
import os
from tkinter import INSERT
from unicodedata import name
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re



connection = sqlite3.connect("music-data.db")

cur = connection.cursor()



with open('client_id.txt') as f:
    client_id = f.read()
    f.close()

with open('client_secret.txt') as f:
    client_secret = f.read()
    f.close()


sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))





def get_input_url():
    inputlink = ""
    print("Enter sharing link for a playlist or song")
    inputlink = input()
    

    
    type = re.findall("playlist|track", inputlink)[0]
    relevantpart = re.findall("/[0-9a-zA-Z]*\?", inputlink)
    id = re.findall("[0-9a-zA-Z]+", relevantpart[0])[0]

    output = [type, id]
    return output

def get_playlist_items(playlist_id):
    result = sp.playlist_items(playlist_id)
    items = result["items"]
    track_list = []
    track_count = 0
    for item in items:
        trackid = item["track"]["id"]
        track_list.append(trackid)
        track_count += 1
        
    output = [track_list, track_count]
    return output

def add_track_db(id):
    
    
    trackname, trackartists, trackalbum, trackduration, trackid = get_track_data(id)


    #write into track list
    count = 0
    readout = cur.execute('SELECT spotify_id FROM tracklist WHERE spotify_id=?', (trackid,))
    for i in readout:
        count += 1
    if count == 0:
        cur.execute('INSERT INTO tracklist (title, spotify_id, duration_ms) VALUES (?,?,?)', (trackname, trackid, trackduration))
    
        # #write into interpret list and track-interpret-relations
        cur.execute('SELECT idtrack FROM tracklist WHERE spotify_id=?', (trackid,))
        idtrack = int(cur.fetchone()[0])
        
        for artistid in trackartists:
            count = 0
            readout = cur.execute('SELECT spotify_id FROM interpreten WHERE spotify_id=?', (artistid,))
            for i in readout:
                count += 1
            if count == 0:
                name = get_artist_data(artistid)
                cur.execute('INSERT INTO interpreten (name, spotify_id) VALUES (?,?)', (name, artistid))

            cur.execute('SELECT idinterpret FROM interpreten WHERE spotify_id=?', (artistid,))
            idinterpret = int(cur.fetchone()[0])

        cur.execute('SELECT idinterpret FROM interpreten WHERE spotify_id=?', (trackartists[0],))
        idinterpret1 = int(cur.fetchone()[0])
        cur.execute('INSERT INTO track_interpret_relations (idtrack, idinterpret) VALUES (?,?)', (idtrack, idinterpret))
        # #write into album list and create relations
        count = 0
        readout = cur.execute('SELECT spotify_id FROM albums WHERE spotify_id=?', (trackalbum,))
        
        for i in readout:
            count += 1
        if count == 0:
            name = get_album_data(trackalbum)
            cur.execute('INSERT INTO albums (album_name, spotify_id) VALUES (?,?)', (name, trackalbum))
            cur.execute('SELECT idalbum FROM albums WHERE spotify_id=?', (trackalbum,))
            idalbum = int(cur.fetchone()[0])
            cur.execute('INSERT INTO album_interpret_relations (idalbum, idinterpret) VALUES (?,?)', (idalbum, idinterpret1))
        else:
            cur.execute('SELECT idalbum FROM albums WHERE spotify_id=?', (trackalbum,))
            idalbum = int(cur.fetchone()[0])
            

        

        cur.execute('INSERT INTO album_track_relations (idalbum, idtrack) VALUES (?,?)', (idalbum, idtrack))

        
        #write into relations

        
        
        





        print("------- ", id, "imported")
    else:
        print("------- ", id, "already in database")
    
def get_track_data(id):
    trackartists = []
    

    raw_data = sp.track(id)

    trackname = raw_data['name']
    
    for key in raw_data['artists']:
        trackartists.append(key['id'])

    trackalbum = raw_data['album']['id']
    trackduration = raw_data['duration_ms']
    trackid = raw_data['id']

    return(trackname, trackartists, trackalbum, trackduration, trackid)

def get_album_data(id):
    raw_data = sp.album(id)
    name = raw_data['name']
    return(name)

def get_artist_data(id):
    raw_data = sp.artist(id)
    name = raw_data['name']
    return(name)



#https://open.spotify.com/track/3mXOssdHHkN6AvLw6ZgKiL?si=e1139c79407844bc = same energy - kid

#example to get info of the song
# result = sp.track("5L0JMH1LRJrsjbjFhWXB3k")
# for key in result:
#     relevant_data = [
#         'name',
#         'artists',
#         'album',
#         'duration_ms',
#         'id'
#     ]
# for data_type in relevant_data:
#     print(result[data_type])


#programm starts here:

items_to_import = []
type, id = get_input_url()
print(type, id)
if type == "playlist":
    items_to_import, item_count = get_playlist_items(id)
else:
    item_count = 1
    items_to_import.append(id)




if item_count == 1:
    print("importing 1 track into database")
    add_track_db(id)
else:
    print("importing", item_count, "tracks into database")
    for i in items_to_import:
        add_track_db(i)


connection.commit()
connection.close()
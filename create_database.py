import sqlite3
import os


try:
	os.remove("music-data.db")
except FileNotFoundError:
	pass

connection = sqlite3.connect("music-data.db")

cur = connection.cursor()

cur.execute("""
	CREATE TABLE tracklist(
		idtrack		INTEGER PRIMARY KEY,
		title		VARCHAR(64),
		spotify_id	VARCHAR(64),
		duration_ms	INTEGER
	);
""")






cur.execute("""
	CREATE TABLE interpreten (
		idinterpret	INTEGER PRIMARY KEY,
		name		VARCHAR(64),
		spotify_id	VARCHAR(64)
	);
""")





cur.execute("""
	CREATE TABLE albums (
		idalbum		INTEGER PRIMARY KEY,
		album_name	VARCHAR(64),
		spotify_id	VARCHAR(64)
	);
""")


cur.execute("""
	CREATE TABLE track_interpret_relations (
		idtrack		INTEGER,
		idinterpret	INTEGER 
	);
""")




cur.execute("""
	CREATE TABLE album_interpret_relations (
		idalbum		INTEGER,
		idinterpret	INTEGER
	);
""")
cur.execute("""
	CREATE TABLE album_track_relations (
		idalbum		INTEGER,
		idtrack		INTEGER 
	);
""")



connection.commit()
connection.close()

print("Database created")
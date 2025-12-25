
import pandas as pd
import math 
import json  
import psycopg2
import os

# Get database connection from environment variable
DATABASE_URL = os.getenv('DATABASE_URL')

# Connect to PostgreSQL
conn = psycopg2.connect(DATABASE_URL)

# Read unindexed songs from database
query = "SELECT song_id, artist, song, clean_lyrics FROM songs WHERE indexed = FALSE"
data = pd.read_sql(query, conn)

print(f"Found {len(data)} unindexed songs")

# creating song document
def create_song_document(data):
    song_document = {}
    for index, row in data.iterrows():
        song_document[row['song_id']] = {

            "song_id" : row['song_id'],
            "song_name" : row['song'],
            "artist" : row['artist'],
            "clean_lyrics" : row['clean_lyrics'],
            "length" : len(row['clean_lyrics'].split())
        }
    return song_document

song_document = create_song_document(data)

song_document_length = len(song_document)
print('song-document-length', song_document_length)

# save song document to json 
with open('song_document.json','w') as f: 
    json.dump(song_document, f, indent=2)
print("✓ Saved song_document.json")


# creating inverted index for words
def create_inverted_index(data, song_document_length):
    word_dict = {}

    for _, row in data.iterrows():
        song_id = row['song_id']
        song_name = row['song']
        lyrics = row['clean_lyrics']
        artist_name = row['artist']

        song_name_words = song_name.lower().split()
        lyrics_words = lyrics.lower().split()
        artist_name_words = artist_name.lower().split()

        song_name_freq = {}
        for word in song_name_words:
            song_name_freq[word] = song_name_freq.get(word, 0) + 1

        lyrics_freq = {}
        for word in lyrics_words:
            lyrics_freq[word] = lyrics_freq.get(word, 0) + 1

        artist_name_freq = {}
        for word in artist_name_words:
            artist_name_freq[word] = artist_name_freq.get(word, 0) + 1

        all_words = (
            set(song_name_freq.keys())
            | set(lyrics_freq.keys())
            | set(artist_name_freq.keys())
        )

        for word in all_words:
            if word not in word_dict:
                word_dict[word] = {'songs': {}}

          
            word_dict[word]['songs'][song_id] = {
                'song_name': song_name_freq.get(word, 0),
                'artist_name': artist_name_freq.get(word, 0),
                'lyrics': lyrics_freq.get(word, 0)
            }

    N = song_document_length

    for word in word_dict:
        df = len(word_dict[word]['songs'])
        if df > 0:
            word_dict[word]['idf'] = math.log(N / df)

    return word_dict

create_inverted_index = create_inverted_index(data,song_document_length)

# save inverted index to json 
with open('inverted_index.json','w') as f: 
    json.dump(create_inverted_index, f, indent=2)
print("✓ Saved inverted_index.json")


# hmm here marking it true will mess things up as json are non appendable & when new data comes in we will only consider the one tagged as False & will ignore the ones tagged as true 
# what we will do is we will rebuild the index once a day or once a month 
# cursor = conn.cursor()
# cursor.execute("UPDATE songs SET indexed = TRUE WHERE indexed = FALSE")
# conn.commit()
# print(f"Marked {cursor.rowcount} songs as indexed")

# # Close connection
# cursor.close()
# conn.close()
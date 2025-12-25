from flask import Flask, request, render_template
import json
import math
from pathlib import Path

app = Flask(__name__)


BASE_DIR = Path.cwd() 
print("Loading data...")

song_document_path = BASE_DIR/'song_document.json'
inverted_index_path = BASE_DIR/'inverted_index.json'

with open(song_document_path, 'r') as f:
    song_document = json.load(f)

with open(inverted_index_path, 'r') as f: 
    inverted_index = json.load(f)

print("Documents are loaded")


def search_songs(query, top_k=3):
    FIELD_WEIGHTS = {
        'song_name': 10.0,
        'lyrics': 1.0,
        'artist_name': 50.0  # match your index key
    }
    
    tokens = query.lower().split()
    if not tokens:
        return []
    
    candidates = {}
    
    for word in tokens:
        if word not in inverted_index:
            continue
        
        idf = inverted_index[word]['idf']
        songs = inverted_index[word]['songs']
        
        for song_id, field_data in songs.items():
            if song_id not in candidates:
                candidates[song_id] = {
                    'score': 0,
                    'matched_words': [],
                    'field_matches': {
                        'song_name': 0,
                        'lyrics': 0,
                        'artist_name': 0  # fix typo and match key
                    }
                }
            
            candidates[song_id]['matched_words'].append(word)
            song_length = song_document[song_id]['length']
            
            for field in ['song_name', 'lyrics', 'artist_name']:
                freq = field_data.get(field, 0)  # use integer directly
                
                if freq > 0:
                    tf = freq / song_length
                    field_score = tf * idf * FIELD_WEIGHTS[field]
                    candidates[song_id]['score'] += field_score
                    candidates[song_id]['field_matches'][field] += 1
    
    sorted_results = sorted(
        candidates.items(),
        key=lambda x: x[1]['score'],
        reverse=True
    )
    
    results = []
    for song_id, data in sorted_results[:top_k]:
        results.append({
            'song_id': song_id,
            'song_name': song_document[song_id]['song_name'],
            'artist': song_document[song_id]['artist'],
            'score': round(data['score'], 4),
            'matched_words': ', '.join(data['matched_words']),
            'title_match': data['field_matches']['song_name'] > 0,
            'lyrics_match': data['field_matches']['lyrics'] > 0
        })
    
    return results



@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Main page - handles both displaying form and processing search
    """
    
    # Default state
    query = ''
    results = []
    searched = False
    
    # If form was submitted (POST request)
    if request.method == 'POST':
        query = request.form.get('query', '').strip()
        searched = True
        
        if query:
            results = search_songs(query, top_k=10)
    
    # Render the template with data
    return render_template(
        'index.html',
        query=query,
        results=results,
        searched=searched
    )


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
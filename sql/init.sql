-- Create the songs table
CREATE TABLE IF NOT EXISTS songs (
    artist VARCHAR(255) NOT NULL,
    song VARCHAR(500) NOT NULL,
    clean_lyrics TEXT NOT NULL,
    created_date TIMESTAMP DEFAULT NOW(),
    indexed BOOLEAN DEFAULT FALSE,
    song_id SERIAL PRIMARY KEY
);

-- Create indexes for faster queries
CREATE INDEX idx_artist ON songs(artist);
CREATE INDEX idx_song_name ON songs(song);
CREATE INDEX idx_indexed ON songs(indexed);

-- Load your CSV into the table
COPY songs(artist, song, clean_lyrics)
FROM '/data/cleaned_data-v2.csv'
DELIMITER ','
CSV HEADER;

-- Mark all as unindexed so your script processes them
UPDATE songs SET indexed = FALSE;

-- Show results
SELECT COUNT(*) as total_songs FROM songs;

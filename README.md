# Music Search App 🎵

A Dockerized Flask application for searching music data with PostgreSQL.  
This app builds an **inverted index** from your data and allows you to search songs via a web interface.

---

## Requirements

- Docker  
- Docker Compose  

---

## Quick Setup

1. **Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/music-search.git
cd music-search
```

2. **Build and start the containers**
```bash
docker compose up --build
```

3. **Open the app in your browser**
```bash
http://127.0.0.1:5000
```

**Project Structure**
```bash
music-search/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── sql/
│   └── init.sql
├── data/
│   └── cleaned_data.csv
├── src/
│   ├── app.py
│   ├── inverted_index_document.py
│   └── templates/
│       └── index.html
├── screenshots/
│   ├── screenshot1.png
│   └── screenshot2.png
└── README.md
```

Notes

Database: PostgreSQL, persists data using Docker volumes.

Index files (song_document.json and inverted_index.json) are generated automatically in src/ at startup.


For development, edit code in src/. Rebuild if you make significant changes:
```bash
docker compose up --build
```

Optional: Stop and Remove Containers

To stop the containers:
```bash
docker compose down
```
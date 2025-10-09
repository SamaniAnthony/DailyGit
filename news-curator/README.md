# 📰 News Curator

A lightweight, powerful, and efficient news aggregation and curation system. Automatically scrape, organize, and browse news from multiple sources with a clean web interface.

## ✨ Features

- **RSS Feed Aggregation**: Automatically fetch from 10+ pre-configured tech, finance, AI, and design sources
- **Web Scraping**: Extract articles from any website (RSS or HTML)
- **Smart Storage**: SQLite database with deduplication and efficient indexing
- **Web Dashboard**: Clean, minimalist interface to browse, filter, and search articles
- **Filtering & Search**: Filter by category, source, read/unread status, starred articles
- **Article Management**: Star important articles, mark as read, track statistics
- **Docker Ready**: One-command deployment with Docker Compose
- **Automatic Updates**: Optional cron job for scheduled feed fetching
- **Lightweight**: Pure Python, minimal dependencies, no heavy frameworks

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone or download the project
cd news-curator

# Build and run with Docker Compose
docker-compose up -d

# Access the dashboard
open http://localhost:8080
```

That's it! The system will:
- Start the web interface on port 8080
- Create a database with default sources
- Set up automatic hourly feed fetching (if using cron container)

### Option 2: Local Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
cd app
python main.py

# Access the dashboard
open http://localhost:8080
```

## 📁 Project Structure

```
news-curator/
├── app/
│   ├── main.py              # FastAPI web application
│   ├── database.py          # SQLite database manager
│   ├── feed_fetcher.py      # RSS/Atom feed parser
│   └── scraper.py           # Web scraping utilities
├── static/
│   ├── css/styles.css       # Minimalist grayscale design
│   └── js/app.js           # Frontend JavaScript
├── templates/
│   ├── index.html          # Main dashboard
│   └── article.html        # Article detail view
├── data/
│   └── news_curator.db     # SQLite database (created automatically)
├── logs/
│   └── app.log             # Application logs
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎯 Usage

### Browse Articles

1. Open `http://localhost:8080`
2. Browse the latest articles from all sources
3. Filter by category, source, or search keywords
4. Click any article to read or view original

### Manage Articles

- **Star**: Save important articles for later
- **Mark as Read**: Track what you've read
- **Search**: Find articles by title or content

### Refresh Feeds

Click "Refresh Feeds" button to manually fetch latest articles, or wait for automatic hourly updates.

### Add New Sources

1. Click "Settings"
2. Fill in the "Add New Source" form:
   - **Name**: Display name
   - **URL**: Website homepage
   - **RSS Feed URL**: RSS/Atom feed URL
   - **Category**: tech, ai, finance, webdev, or design
3. Click "Add Source"

## 📡 Pre-configured Sources

The system comes with these default sources:

### Tech News
- Hacker News
- TechCrunch
- Ars Technica
- The Verge
- Reuters Technology

### AI/ML
- MIT Technology Review AI

### Finance
- WSJ Markets
- Financial Times

### Web Development
- CSS Tricks
- Smashing Magazine

### Design
- Designer News

## 🔧 API Endpoints

### Articles
- `GET /api/articles` - Get articles (with filters)
- `GET /api/article/{id}` - Get single article
- `POST /api/article/{id}/read` - Mark as read
- `POST /api/article/{id}/star` - Toggle star
- `DELETE /api/articles/cleanup?days=30` - Delete old articles

### Sources
- `GET /api/sources` - List all sources
- `POST /api/sources` - Add new source

### Operations
- `POST /api/fetch` - Fetch all feeds
- `GET /api/stats` - Get statistics
- `GET /health` - Health check

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (optional):

```bash
DATABASE_PATH=data/news_curator.db
LOG_LEVEL=INFO
FETCH_TIMEOUT=30
```

### Cron Schedule

Edit `crontab` to change fetch frequency:

```cron
# Every hour
0 * * * * curl -X POST http://news-curator:8080/api/fetch

# Every 15 minutes
*/15 * * * * curl -X POST http://news-curator:8080/api/fetch
```

## 🐳 Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Access shell
docker exec -it news-curator sh
```

## 📊 Database

SQLite database with efficient schema:

**Tables:**
- `articles` - Stores all fetched articles with metadata
- `sources` - RSS feeds and websites to scrape
- `keywords` - Custom keywords for filtering (future use)

**Features:**
- URL hashing for deduplication
- Indexed queries for fast filtering
- Automatic cleanup of old articles (keeps starred)

## 🔍 Advanced Usage

### Custom Web Scraper

To scrape a non-RSS website:

```python
from app.scraper import WebScraper

scraper = WebScraper()
article = scraper.extract_article(
    url="https://example.com/article",
    source_name="Example Site",
    category="tech"
)
```

### Manual Feed Fetch

```python
from app.feed_fetcher import FeedFetcher
from app.database import Database

fetcher = FeedFetcher()
db = Database()

articles = fetcher.fetch_feed(
    feed_url="https://example.com/feed.xml",
    source_name="Example",
    category="tech"
)

for article in articles:
    db.add_article(article)
```

### Database Queries

```python
from app.database import Database

db = Database()

# Get unread tech articles
articles = db.get_articles(
    category="tech",
    unread_only=True,
    limit=20
)

# Get statistics
stats = db.get_stats()
print(f"Total: {stats['total_articles']}")
```

## 🛠️ Development

### Run in Development Mode

```bash
cd app
uvicorn main:app --reload --port 8080
```

### Add New Dependencies

```bash
pip install package-name
pip freeze > requirements.txt
```

### Run Tests (TODO)

```bash
pytest tests/
```

## 📈 Performance

- **Lightweight**: ~50MB Docker image
- **Fast**: Sub-second page loads
- **Efficient**: Indexed database queries
- **Scalable**: Handles 1000+ articles easily

## 🔒 Security

- No external data sharing
- All data stored locally
- No authentication required (single-user system)
- For production: Add nginx reverse proxy + HTTPS

## 🐛 Troubleshooting

### Articles not loading?

1. Check if feeds are fetched: Click "Refresh Feeds"
2. Check logs: `docker-compose logs -f`
3. Verify database exists: `ls data/`

### Feed fetch failing?

1. Check internet connection
2. Verify feed URL is valid RSS/Atom
3. Check logs for specific errors

### Port 8080 already in use?

Change port in `docker-compose.yml`:
```yaml
ports:
  - "8081:8080"  # Use 8081 instead
```

## 🚀 Deployment

### VPS Deployment (DigitalOcean, Linode, etc.)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone project
git clone <your-repo>
cd news-curator

# Run
docker-compose up -d

# Access via IP
http://YOUR_IP:8080
```

### Add Domain & HTTPS

Use nginx reverse proxy:

```nginx
server {
    listen 80;
    server_name news.yourdomain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then add SSL with Let's Encrypt:
```bash
certbot --nginx -d news.yourdomain.com
```

## 📝 Roadmap

- [ ] Email digest notifications
- [ ] AI-powered article summarization
- [ ] Relevance scoring based on keywords
- [ ] Multi-user support with authentication
- [ ] Browser extension for one-click save
- [ ] Export to Pocket, Instapaper, etc.
- [ ] Mobile-responsive design improvements
- [ ] Dark mode

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - feel free to use for personal or commercial projects.

## 💬 Support

For issues or questions:
- Create an issue on GitHub
- Check logs: `docker-compose logs -f`
- Review API docs: `http://localhost:8080/docs`

---

**Built with:**
- Python 3.11
- FastAPI
- SQLite
- BeautifulSoup
- Feedparser
- Docker

Enjoy your automated news curation! 📰✨

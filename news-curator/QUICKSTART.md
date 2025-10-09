# 🚀 Quick Start Guide

Get News Curator running in 2 minutes!

## Method 1: Docker (Easiest)

```bash
# Navigate to project
cd news-curator

# Start the application
docker-compose up -d

# Open in browser
open http://localhost:8080
```

Done! The app is now running.

## Method 2: Local Python

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the app
cd app
python3 main.py

# Open in browser
open http://localhost:8080
```

## Method 3: One-Line Startup

```bash
# Make script executable
chmod +x run.sh

# Run it
./run.sh
```

---

## First Steps

Once the app is running:

### 1. Fetch Your First Articles

Click the **"Refresh Feeds"** button in the dashboard. Wait 10-30 seconds, then refresh the page.

You should see articles from:
- Hacker News
- TechCrunch
- Ars Technica
- And more!

### 2. Browse and Filter

- **Filter by category**: Tech, AI, Finance, Web Dev, Design
- **Filter by source**: Choose specific publications
- **Search**: Find articles by keyword
- **Star articles**: Save favorites
- **Mark as read**: Track your reading

### 3. Customize Sources

Click **"Settings"** → **"Add New Source"**

You need:
- **Name**: E.g., "My Favorite Blog"
- **URL**: Website homepage
- **RSS Feed URL**: The feed URL (usually ends in `/feed`, `/rss`, or `/feed.xml`)
- **Category**: Choose one

**Finding RSS Feeds:**
- Look for RSS icon on website
- Try adding `/feed` or `/rss` to URL
- Use browser extension: "RSS Feed Reader"
- Check page source for `<link type="application/rss+xml">`

---

## Common Tasks

### Stop the App

```bash
# Docker
docker-compose down

# Local Python
# Press Ctrl+C in terminal
```

### View Logs

```bash
# Docker
docker-compose logs -f

# Local Python
tail -f logs/app.log
```

### Clean Old Articles

In the dashboard:
1. Click "Settings"
2. Click "Delete Articles Older Than 30 Days"

Or via API:
```bash
curl -X DELETE http://localhost:8080/api/articles/cleanup?days=30
```

### Backup Database

```bash
cp data/news_curator.db data/backup_$(date +%Y%m%d).db
```

---

## Troubleshooting

### No articles showing?

1. Click "Refresh Feeds" button
2. Wait 30 seconds
3. Refresh browser page
4. Check logs: `docker-compose logs -f`

### Can't access http://localhost:8080?

1. Check if app is running: `docker ps` or check terminal
2. Try `http://127.0.0.1:8080`
3. Check if port is in use: `lsof -i :8080`
4. Change port in `docker-compose.yml` if needed

### "Module not found" error?

```bash
pip3 install -r requirements.txt
```

---

## What's Next?

- **Add more sources**: Settings → Add New Source
- **Set up auto-fetch**: The cron container runs hourly
- **Deploy to server**: See main README for VPS deployment
- **Customize**: Edit `static/css/styles.css` for your style

Enjoy! 📰✨

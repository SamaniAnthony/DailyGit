"""
FastAPI Web Dashboard for News Curator
Lightweight, fast API and web interface
"""

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from typing import Optional, List
import uvicorn
from pathlib import Path
import logging

from .database import Database
from .feed_fetcher import FeedFetcher, DEFAULT_SOURCES
from .scraper import WebScraper

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="News Curator",
    description="Lightweight news aggregation and curation system",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Initialize components
db = Database()
feed_fetcher = FeedFetcher()
scraper = WebScraper()


# ===========================
# Web Interface Routes
# ===========================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main dashboard page"""
    stats = db.get_stats()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "stats": stats
    })


@app.get("/article/{article_id}", response_class=HTMLResponse)
async def article_view(request: Request, article_id: int):
    """View single article"""
    article = db.get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    # Mark as read
    db.mark_as_read(article_id)

    return templates.TemplateResponse("article.html", {
        "request": request,
        "article": article
    })


# ===========================
# API Routes
# ===========================

@app.get("/api/articles")
async def get_articles(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    category: Optional[str] = None,
    source: Optional[str] = None,
    starred: bool = False,
    unread: bool = False,
    search: Optional[str] = None
):
    """Get articles with filtering"""
    articles = db.get_articles(
        limit=limit,
        offset=offset,
        category=category,
        source=source,
        starred_only=starred,
        unread_only=unread,
        search=search
    )
    return {"articles": articles, "count": len(articles)}


@app.get("/api/article/{article_id}")
async def get_article(article_id: int):
    """Get single article"""
    article = db.get_article_by_id(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@app.post("/api/article/{article_id}/read")
async def mark_read(article_id: int):
    """Mark article as read"""
    success = db.mark_as_read(article_id)
    if not success:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"status": "success"}


@app.post("/api/article/{article_id}/star")
async def toggle_star(article_id: int):
    """Toggle star status"""
    success = db.toggle_star(article_id)
    if not success:
        raise HTTPException(status_code=404, detail="Article not found")

    article = db.get_article_by_id(article_id)
    return {"status": "success", "is_starred": article['is_starred']}


@app.get("/api/stats")
async def get_stats():
    """Get database statistics"""
    return db.get_stats()


@app.get("/api/sources")
async def get_sources(active_only: bool = True):
    """Get all sources"""
    if active_only:
        sources = db.get_active_sources()
    else:
        sources = db.get_all_sources()
    return {"sources": sources}


@app.post("/api/sources")
async def add_source(source: dict):
    """Add new source"""
    try:
        source_id = db.add_source(source)
        return {"status": "success", "id": source_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/api/fetch")
async def fetch_feeds(background_tasks: BackgroundTasks):
    """Fetch all active feeds in background"""
    background_tasks.add_task(fetch_all_feeds)
    return {"status": "started", "message": "Fetching feeds in background"}


@app.post("/api/fetch/{source_id}")
async def fetch_single_source(source_id: int, background_tasks: BackgroundTasks):
    """Fetch single source"""
    sources = db.get_all_sources()
    source = next((s for s in sources if s['id'] == source_id), None)

    if not source:
        raise HTTPException(status_code=404, detail="Source not found")

    background_tasks.add_task(fetch_source, source)
    return {"status": "started", "message": f"Fetching {source['name']}"}


@app.delete("/api/articles/cleanup")
async def cleanup_articles(days: int = Query(30, ge=1, le=365)):
    """Delete old articles (keep starred)"""
    deleted = db.cleanup_old_articles(days)
    return {"status": "success", "deleted": deleted}


@app.get("/api/categories")
async def get_categories():
    """Get all unique categories"""
    stats = db.get_stats()
    categories = list(stats.get('by_category', {}).keys())
    return {"categories": categories}


# ===========================
# Background Tasks
# ===========================

async def fetch_all_feeds():
    """Fetch all active feeds"""
    logger.info("Starting feed fetch job")

    sources = db.get_active_sources()
    total_added = 0

    for source in sources:
        try:
            articles = fetch_source(source)
            total_added += articles
        except Exception as e:
            logger.error(f"Error fetching {source['name']}: {e}")

    logger.info(f"Feed fetch complete. Added {total_added} new articles")


def fetch_source(source: dict) -> int:
    """Fetch single source and store articles"""
    logger.info(f"Fetching {source['name']}")

    added_count = 0

    try:
        if source['source_type'] == 'rss' and source.get('feed_url'):
            articles = feed_fetcher.fetch_feed(
                source['feed_url'],
                source['name'],
                source.get('category')
            )

            for article in articles:
                article_id = db.add_article(article)
                if article_id:
                    added_count += 1

        # Update last fetched time
        db.update_source_fetch_time(source['id'])

    except Exception as e:
        logger.error(f"Error fetching source {source['name']}: {e}")

    logger.info(f"Added {added_count} new articles from {source['name']}")
    return added_count


# ===========================
# Startup/Shutdown Events
# ===========================

@app.on_event("startup")
async def startup_event():
    """Initialize database and add default sources"""
    logger.info("Starting News Curator")

    # Create necessary directories
    Path("data").mkdir(exist_ok=True)
    Path("logs").mkdir(exist_ok=True)

    # Add default sources if database is empty
    existing_sources = db.get_all_sources()
    if not existing_sources:
        logger.info("Adding default sources")
        for source in DEFAULT_SOURCES:
            db.add_source(source)

    # Initial fetch (optional - uncomment to fetch on startup)
    # await fetch_all_feeds()


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down News Curator")


# ===========================
# Health Check
# ===========================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "news-curator"}


# ===========================
# Run Application
# ===========================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )

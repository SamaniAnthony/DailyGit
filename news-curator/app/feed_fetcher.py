"""
RSS Feed and News Fetcher
Handles RSS/Atom feeds and extracts article data
"""

import feedparser
import requests
from datetime import datetime
from typing import List, Dict, Optional
import logging
from urllib.parse import urljoin
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeedFetcher:
    """Fetch and parse RSS/Atom feeds"""

    def __init__(self, timeout: int = 30, user_agent: str = None):
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (compatible; NewsCurator/1.0; +http://example.com/bot)"
        )

    def fetch_feed(self, feed_url: str, source_name: str, category: str = None) -> List[Dict]:
        """
        Fetch and parse RSS/Atom feed

        Args:
            feed_url: URL of the RSS/Atom feed
            source_name: Name of the source
            category: Category to assign to articles

        Returns:
            List of article dictionaries
        """
        articles = []

        try:
            logger.info(f"Fetching feed: {feed_url}")

            # Set custom user agent
            feedparser.USER_AGENT = self.user_agent

            # Parse feed with timeout
            feed = feedparser.parse(
                feed_url,
                request_headers={"User-Agent": self.user_agent}
            )

            if feed.bozo:
                logger.warning(f"Feed parsing warning for {feed_url}: {feed.bozo_exception}")

            # Extract articles from entries
            for entry in feed.entries:
                article = self._parse_entry(entry, source_name, category)
                if article:
                    articles.append(article)

            logger.info(f"Fetched {len(articles)} articles from {source_name}")

        except Exception as e:
            logger.error(f"Error fetching feed {feed_url}: {e}")

        return articles

    def _parse_entry(self, entry, source_name: str, category: str = None) -> Optional[Dict]:
        """Parse individual feed entry into article dict"""
        try:
            # Extract URL
            url = entry.get('link') or entry.get('id')
            if not url:
                return None

            # Extract title
            title = entry.get('title', 'No Title')

            # Extract content/summary
            content = self._extract_content(entry)
            summary = entry.get('summary', '')[:500]  # Limit summary length

            # Extract author
            author = entry.get('author') or entry.get('dc:creator')

            # Extract published date
            published_date = self._parse_date(entry)

            # Extract image URL
            image_url = self._extract_image(entry)

            # Extract tags
            tags = self._extract_tags(entry)

            article = {
                'url': url,
                'title': title,
                'content': content,
                'summary': summary,
                'author': author,
                'source_name': source_name,
                'category': category,
                'tags': tags,
                'published_date': published_date,
                'image_url': image_url,
                'relevance_score': 0.0
            }

            return article

        except Exception as e:
            logger.error(f"Error parsing entry: {e}")
            return None

    def _extract_content(self, entry) -> str:
        """Extract content from entry"""
        # Try different content fields
        if hasattr(entry, 'content') and entry.content:
            return entry.content[0].value

        if hasattr(entry, 'description'):
            return entry.description

        if hasattr(entry, 'summary'):
            return entry.summary

        return ""

    def _parse_date(self, entry) -> Optional[str]:
        """Parse published date from entry"""
        # Try different date fields
        for date_field in ['published_parsed', 'updated_parsed', 'created_parsed']:
            if hasattr(entry, date_field):
                time_struct = getattr(entry, date_field)
                if time_struct:
                    try:
                        dt = datetime(*time_struct[:6])
                        return dt.isoformat()
                    except:
                        pass

        # Try string date fields
        for date_field in ['published', 'updated', 'created']:
            if hasattr(entry, date_field):
                date_str = getattr(entry, date_field)
                if date_str:
                    return date_str

        return None

    def _extract_image(self, entry) -> Optional[str]:
        """Extract image URL from entry"""
        # Try media content
        if hasattr(entry, 'media_content') and entry.media_content:
            for media in entry.media_content:
                if media.get('type', '').startswith('image'):
                    return media.get('url')

        # Try media thumbnail
        if hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
            return entry.media_thumbnail[0].get('url')

        # Try enclosures
        if hasattr(entry, 'enclosures') and entry.enclosures:
            for enclosure in entry.enclosures:
                if enclosure.get('type', '').startswith('image'):
                    return enclosure.get('href')

        # Try links
        if hasattr(entry, 'links'):
            for link in entry.links:
                if link.get('type', '').startswith('image'):
                    return link.get('href')

        return None

    def _extract_tags(self, entry) -> List[str]:
        """Extract tags from entry"""
        tags = []

        if hasattr(entry, 'tags'):
            for tag in entry.tags:
                if isinstance(tag, dict):
                    tags.append(tag.get('term', ''))
                else:
                    tags.append(str(tag))

        # Also check category field
        if hasattr(entry, 'category'):
            tags.append(entry.category)

        return [tag for tag in tags if tag]  # Filter empty strings

    def fetch_multiple_feeds(self, sources: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Fetch multiple feeds

        Args:
            sources: List of source dicts with feed_url, name, category

        Returns:
            Dict mapping source name to list of articles
        """
        results = {}

        for source in sources:
            if source.get('source_type') != 'rss':
                continue

            feed_url = source.get('feed_url')
            if not feed_url:
                continue

            articles = self.fetch_feed(
                feed_url,
                source['name'],
                source.get('category')
            )

            results[source['name']] = articles

            # Be nice to servers
            time.sleep(1)

        return results


# Pre-configured popular sources
DEFAULT_SOURCES = [
    # Tech News
    {
        "name": "Hacker News",
        "url": "https://news.ycombinator.com",
        "feed_url": "https://news.ycombinator.com/rss",
        "category": "tech",
        "source_type": "rss"
    },
    {
        "name": "TechCrunch",
        "url": "https://techcrunch.com",
        "feed_url": "https://techcrunch.com/feed/",
        "category": "tech",
        "source_type": "rss"
    },
    {
        "name": "Ars Technica",
        "url": "https://arstechnica.com",
        "feed_url": "https://feeds.arstechnica.com/arstechnica/index",
        "category": "tech",
        "source_type": "rss"
    },
    {
        "name": "The Verge",
        "url": "https://www.theverge.com",
        "feed_url": "https://www.theverge.com/rss/index.xml",
        "category": "tech",
        "source_type": "rss"
    },

    # AI/ML
    {
        "name": "MIT Technology Review AI",
        "url": "https://www.technologyreview.com/topic/artificial-intelligence/",
        "feed_url": "https://www.technologyreview.com/topic/artificial-intelligence/feed",
        "category": "ai",
        "source_type": "rss"
    },

    # Finance
    {
        "name": "WSJ Markets",
        "url": "https://www.wsj.com/news/markets",
        "feed_url": "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml",
        "category": "finance",
        "source_type": "rss"
    },
    {
        "name": "Financial Times",
        "url": "https://www.ft.com",
        "feed_url": "https://www.ft.com/?format=rss",
        "category": "finance",
        "source_type": "rss"
    },

    # Web Development
    {
        "name": "CSS Tricks",
        "url": "https://css-tricks.com",
        "feed_url": "https://css-tricks.com/feed/",
        "category": "webdev",
        "source_type": "rss"
    },
    {
        "name": "Smashing Magazine",
        "url": "https://www.smashingmagazine.com",
        "feed_url": "https://www.smashingmagazine.com/feed/",
        "category": "webdev",
        "source_type": "rss"
    },

    # Design
    {
        "name": "Designer News",
        "url": "https://www.designernews.co",
        "feed_url": "https://www.designernews.co/?format=rss",
        "category": "design",
        "source_type": "rss"
    },

    # General News
    {
        "name": "Reuters Technology",
        "url": "https://www.reuters.com/technology",
        "feed_url": "https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best",
        "category": "tech",
        "source_type": "rss"
    }
]

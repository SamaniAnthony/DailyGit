"""
Web Scraper for non-RSS sources
Uses BeautifulSoup for HTML parsing
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging
from datetime import datetime
from urllib.parse import urljoin, urlparse
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraper:
    """General-purpose web scraper"""

    def __init__(self, timeout: int = 30, user_agent: str = None):
        self.timeout = timeout
        self.user_agent = user_agent or (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse HTML page"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            return None

    def extract_article(self, url: str, source_name: str, category: str = None) -> Optional[Dict]:
        """
        Extract article from URL

        This is a generic extractor. For better results, use source-specific parsers.
        """
        soup = self.fetch_page(url)
        if not soup:
            return None

        try:
            # Try to extract title
            title = self._extract_title(soup)

            # Try to extract content
            content = self._extract_content(soup)

            # Try to extract author
            author = self._extract_author(soup)

            # Try to extract published date
            published_date = self._extract_date(soup)

            # Try to extract image
            image_url = self._extract_image(soup, url)

            # Generate summary
            summary = content[:500] if content else ""

            article = {
                'url': url,
                'title': title,
                'content': content,
                'summary': summary,
                'author': author,
                'source_name': source_name,
                'category': category,
                'tags': [],
                'published_date': published_date,
                'image_url': image_url,
                'relevance_score': 0.0
            }

            return article

        except Exception as e:
            logger.error(f"Error extracting article from {url}: {e}")
            return None

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title from page"""
        # Try different selectors
        selectors = [
            'h1',
            'article h1',
            '.article-title',
            '.post-title',
            'meta[property="og:title"]',
            'title'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                if element.name == 'meta':
                    return element.get('content', '')
                return element.get_text(strip=True)

        return "No Title"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from page"""
        # Try different content selectors
        selectors = [
            'article',
            '.article-content',
            '.post-content',
            '.entry-content',
            'main',
            '.content'
        ]

        for selector in selectors:
            element = soup.select_one(selector)
            if element:
                # Remove script and style tags
                for tag in element(['script', 'style', 'nav', 'footer', 'aside']):
                    tag.decompose()
                return element.get_text(strip=True, separator='\n')

        # Fallback: get all paragraph text
        paragraphs = soup.find_all('p')
        return '\n'.join([p.get_text(strip=True) for p in paragraphs])

    def _extract_author(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract author from page"""
        # Try meta tags first
        meta_selectors = [
            'meta[name="author"]',
            'meta[property="article:author"]',
            'meta[name="DC.creator"]'
        ]

        for selector in meta_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get('content', '')

        # Try common class names
        author_selectors = [
            '.author',
            '.by-author',
            '.article-author',
            'a[rel="author"]'
        ]

        for selector in author_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get_text(strip=True)

        return None

    def _extract_date(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract published date from page"""
        # Try meta tags
        meta_selectors = [
            'meta[property="article:published_time"]',
            'meta[name="publication_date"]',
            'meta[name="DC.date"]'
        ]

        for selector in meta_selectors:
            element = soup.select_one(selector)
            if element:
                return element.get('content', '')

        # Try time tags
        time_element = soup.select_one('time[datetime]')
        if time_element:
            return time_element.get('datetime', '')

        return None

    def _extract_image(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Extract main image from page"""
        # Try meta tags
        meta_selectors = [
            'meta[property="og:image"]',
            'meta[name="twitter:image"]'
        ]

        for selector in meta_selectors:
            element = soup.select_one(selector)
            if element:
                img_url = element.get('content', '')
                return urljoin(base_url, img_url)

        # Try article images
        article = soup.select_one('article')
        if article:
            img = article.select_one('img')
            if img and img.get('src'):
                return urljoin(base_url, img['src'])

        # Fallback to first image
        img = soup.select_one('img')
        if img and img.get('src'):
            return urljoin(base_url, img['src'])

        return None

    def scrape_list_page(self, url: str, source_name: str, category: str = None) -> List[Dict]:
        """
        Scrape a list/index page to get article URLs

        Returns list of article URLs with metadata
        """
        soup = self.fetch_page(url)
        if not soup:
            return []

        articles = []

        # Find all links
        links = soup.find_all('a', href=True)

        for link in links:
            href = link['href']

            # Skip navigation, social, etc.
            if any(skip in href.lower() for skip in ['#', 'mailto:', 'javascript:', 'twitter.com', 'facebook.com']):
                continue

            # Make absolute URL
            full_url = urljoin(url, href)

            # Basic filter: only links from same domain
            if urlparse(full_url).netloc != urlparse(url).netloc:
                continue

            # Try to extract title from link
            title = link.get_text(strip=True)
            if not title or len(title) < 10:
                continue

            articles.append({
                'url': full_url,
                'title': title,
                'source_name': source_name,
                'category': category
            })

        logger.info(f"Found {len(articles)} potential articles from {url}")
        return articles


class NewspaperExtractor:
    """
    Advanced article extractor using newspaper3k library
    (optional, requires: pip install newspaper3k)
    """

    def __init__(self):
        try:
            from newspaper import Article
            self.Article = Article
            self.available = True
        except ImportError:
            logger.warning("newspaper3k not installed. Advanced extraction unavailable.")
            self.available = False

    def extract_article(self, url: str, source_name: str, category: str = None) -> Optional[Dict]:
        """Extract article using newspaper3k"""
        if not self.available:
            return None

        try:
            article = self.Article(url)
            article.download()
            article.parse()

            # Try NLP features
            try:
                article.nlp()
            except:
                pass

            return {
                'url': url,
                'title': article.title,
                'content': article.text,
                'summary': article.summary if hasattr(article, 'summary') else article.text[:500],
                'author': ', '.join(article.authors) if article.authors else None,
                'source_name': source_name,
                'category': category,
                'tags': list(article.keywords) if hasattr(article, 'keywords') else [],
                'published_date': article.publish_date.isoformat() if article.publish_date else None,
                'image_url': article.top_image,
                'relevance_score': 0.0
            }

        except Exception as e:
            logger.error(f"Error extracting with newspaper3k: {e}")
            return None

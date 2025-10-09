"""
Database models and utilities for news curator
SQLite-based storage with efficient indexing
"""

import sqlite3
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from contextlib import contextmanager
import json


class Database:
    """Lightweight SQLite database manager"""

    def __init__(self, db_path: str = "data/news_curator.db"):
        self.db_path = db_path
        self.init_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def init_database(self):
        """Initialize database schema"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Articles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    url_hash TEXT UNIQUE NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT,
                    summary TEXT,
                    author TEXT,
                    source_name TEXT NOT NULL,
                    category TEXT,
                    tags TEXT,
                    published_date TIMESTAMP,
                    scraped_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_read INTEGER DEFAULT 0,
                    is_starred INTEGER DEFAULT 0,
                    relevance_score REAL DEFAULT 0.0,
                    image_url TEXT,
                    UNIQUE(url_hash)
                )
            """)

            # Sources table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    url TEXT NOT NULL,
                    feed_url TEXT,
                    source_type TEXT DEFAULT 'rss',
                    category TEXT,
                    is_active INTEGER DEFAULT 1,
                    last_fetched TIMESTAMP,
                    fetch_interval INTEGER DEFAULT 3600,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Keywords table for filtering
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    keyword TEXT UNIQUE NOT NULL,
                    category TEXT,
                    weight REAL DEFAULT 1.0,
                    is_active INTEGER DEFAULT 1
                )
            """)

            # Create indexes for performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_published
                ON articles(published_date DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_category
                ON articles(category)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_source
                ON articles(source_name)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_starred
                ON articles(is_starred)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_articles_url_hash
                ON articles(url_hash)
            """)

    @staticmethod
    def hash_url(url: str) -> str:
        """Generate hash of URL for deduplication"""
        return hashlib.md5(url.encode()).hexdigest()

    def add_article(self, article: Dict) -> Optional[int]:
        """Add article to database, returns article ID or None if duplicate"""
        url_hash = self.hash_url(article['url'])

        with self.get_connection() as conn:
            cursor = conn.cursor()

            try:
                cursor.execute("""
                    INSERT INTO articles (
                        url, url_hash, title, content, summary, author,
                        source_name, category, tags, published_date,
                        relevance_score, image_url
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    article['url'],
                    url_hash,
                    article['title'],
                    article.get('content'),
                    article.get('summary'),
                    article.get('author'),
                    article['source_name'],
                    article.get('category'),
                    json.dumps(article.get('tags', [])) if article.get('tags') else None,
                    article.get('published_date'),
                    article.get('relevance_score', 0.0),
                    article.get('image_url')
                ))
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # Article already exists
                return None

    def get_articles(
        self,
        limit: int = 50,
        offset: int = 0,
        category: Optional[str] = None,
        source: Optional[str] = None,
        starred_only: bool = False,
        unread_only: bool = False,
        search: Optional[str] = None
    ) -> List[Dict]:
        """Get articles with filtering options"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            query = "SELECT * FROM articles WHERE 1=1"
            params = []

            if category:
                query += " AND category = ?"
                params.append(category)

            if source:
                query += " AND source_name = ?"
                params.append(source)

            if starred_only:
                query += " AND is_starred = 1"

            if unread_only:
                query += " AND is_read = 0"

            if search:
                query += " AND (title LIKE ? OR content LIKE ?)"
                search_term = f"%{search}%"
                params.extend([search_term, search_term])

            query += " ORDER BY published_date DESC LIMIT ? OFFSET ?"
            params.extend([limit, offset])

            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_article_by_id(self, article_id: int) -> Optional[Dict]:
        """Get single article by ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_article(self, article_id: int, updates: Dict) -> bool:
        """Update article fields"""
        if not updates:
            return False

        with self.get_connection() as conn:
            cursor = conn.cursor()

            fields = ", ".join([f"{k} = ?" for k in updates.keys()])
            query = f"UPDATE articles SET {fields} WHERE id = ?"
            params = list(updates.values()) + [article_id]

            cursor.execute(query, params)
            return cursor.rowcount > 0

    def mark_as_read(self, article_id: int) -> bool:
        """Mark article as read"""
        return self.update_article(article_id, {"is_read": 1})

    def toggle_star(self, article_id: int) -> bool:
        """Toggle star status"""
        article = self.get_article_by_id(article_id)
        if article:
            new_value = 0 if article['is_starred'] else 1
            return self.update_article(article_id, {"is_starred": new_value})
        return False

    def add_source(self, source: Dict) -> int:
        """Add new source"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT OR REPLACE INTO sources (
                    name, url, feed_url, source_type, category,
                    is_active, fetch_interval
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                source['name'],
                source['url'],
                source.get('feed_url'),
                source.get('source_type', 'rss'),
                source.get('category'),
                source.get('is_active', 1),
                source.get('fetch_interval', 3600)
            ))
            return cursor.lastrowid

    def get_active_sources(self) -> List[Dict]:
        """Get all active sources"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM sources
                WHERE is_active = 1
                ORDER BY name
            """)
            return [dict(row) for row in cursor.fetchall()]

    def get_all_sources(self) -> List[Dict]:
        """Get all sources"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sources ORDER BY name")
            return [dict(row) for row in cursor.fetchall()]

    def update_source_fetch_time(self, source_id: int):
        """Update last fetched timestamp"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE sources
                SET last_fetched = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (source_id,))

    def get_stats(self) -> Dict:
        """Get database statistics"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            stats = {}

            # Total articles
            cursor.execute("SELECT COUNT(*) FROM articles")
            stats['total_articles'] = cursor.fetchone()[0]

            # Unread articles
            cursor.execute("SELECT COUNT(*) FROM articles WHERE is_read = 0")
            stats['unread_articles'] = cursor.fetchone()[0]

            # Starred articles
            cursor.execute("SELECT COUNT(*) FROM articles WHERE is_starred = 1")
            stats['starred_articles'] = cursor.fetchone()[0]

            # Articles by category
            cursor.execute("""
                SELECT category, COUNT(*) as count
                FROM articles
                GROUP BY category
            """)
            stats['by_category'] = {row['category']: row['count'] for row in cursor.fetchall()}

            # Active sources
            cursor.execute("SELECT COUNT(*) FROM sources WHERE is_active = 1")
            stats['active_sources'] = cursor.fetchone()[0]

            return stats

    def cleanup_old_articles(self, days: int = 30) -> int:
        """Delete articles older than specified days"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM articles
                WHERE is_starred = 0
                AND published_date < datetime('now', '-' || ? || ' days')
            """, (days,))
            return cursor.rowcount

    def add_keyword(self, keyword: str, category: Optional[str] = None, weight: float = 1.0):
        """Add keyword for filtering"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO keywords (keyword, category, weight)
                VALUES (?, ?, ?)
            """, (keyword.lower(), category, weight))

    def get_keywords(self) -> List[Dict]:
        """Get all active keywords"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM keywords
                WHERE is_active = 1
                ORDER BY category, keyword
            """)
            return [dict(row) for row in cursor.fetchall()]

import asyncio
import feedparser
import httpx
from typing import List, Dict
from pydantic import BaseModel
from utils.logger import setup_logger
from utils.resiliency import safe_execute

logger = setup_logger("scanner")

class Trend(BaseModel):
    source: str
    title: str
    link: str
    summary: str
    timestamp: str

class Scanner:
    def __init__(self):
        self.sources = [
            "https://news.ycombinator.com/rss",
            "https://feeds.feedburner.com/TechCrunch/",
            "https://www.theverge.com/rss/index.xml",
            "https://dev.to/feed"
        ]
        self.seen_urls = set()

    async def fetch_rss(self, url: str) -> List[Trend]:
        """
        Fetches and parses an RSS feed using feedparser (blocking, run in executor).
        """
        logger.info(f"Scanning {url}...")
        try:
            # feedparser fetch is blocking, so we wrap it
            feed = await asyncio.to_thread(feedparser.parse, url)
            trends = []
            if not feed.entries:
                logger.warning(f"No entries found for {url}")
                return []

            for entry in feed.entries[:5]: # Top 5 only for MVP
                if entry.link in self.seen_urls:
                    continue
                
                trend = Trend(
                    source=url,
                    title=entry.get('title', 'No Title'),
                    link=entry.get('link', ''),
                    summary=entry.get('summary', '')[:200], # Truncate summary
                    timestamp=str(entry.get('published', ''))
                )
                self.seen_urls.add(entry.link)
                trends.append(trend)
            
            return trends
        except Exception as e:
            logger.error(f"Error scanning {url}: {e}")
            return []

    async def scan(self) -> List[Trend]:
        """
        Scans all configured sources.
        """
        logger.info("Starting Scan Phase...")
        tasks = [self.fetch_rss(url) for url in self.sources]
        results = await asyncio.gather(*tasks)
        
        # Flatten list
        all_trends = [item for sublist in results for item in sublist]
        logger.info(f"Scan complete. Found {len(all_trends)} new trends.")
        return all_trends

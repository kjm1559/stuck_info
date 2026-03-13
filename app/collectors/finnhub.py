"""Finnhub News Collector with async HTTP client."""
import httpx
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class FinnhubArticle(BaseModel):
    """Finnhub news article model."""
    datetime: int
    headline: str
    id: str
    image: str
    related: List[str]
    source: str
    summary: str
    url: str
    category: str


class FinnhubCollector:
    """Finnhub news collector with async HTTP client."""

    BASE_URL = "https://finnhub.io/api/v1/company-news"

    def __init__(self, api_key: str, timeout: float = 10.0):
        self.api_key = api_key
        self.timeout = timeout

    async def get_company_news(
        self,
        symbol: str,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Fetch news articles for a company.

        Args:
            symbol: Stock ticker symbol
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)

        Returns:
            List of normalized news articles
        """
        url = f"{self.BASE_URL}?symbol={symbol}&from={from_date}&to={to_date}&token={self.api_key}"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()

                articles = response.json()

                if not articles:
                    return []

                normalized = []
                for article in articles:
                    norm_article = self._normalize_article(article)
                    normalized.append(norm_article)

                return normalized

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {symbol}: {e}")
            return []
        except httpx.RequestError as e:
            logger.error(f"Request error for {symbol}: {e}")
            return []
        except Exception as e:
            logger.error(f"Error fetching news for {symbol}: {e}")
            return []

    def _normalize_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Finnhub article to common schema."""
        return {
            "title": article.get("headline", ""),
            "description": article.get("summary", ""),
            "url": article.get("url", ""),
            "image": article.get("image", ""),
            "content": "",
            "source": "finnhub",
            "published_at": datetime.utcfromtimestamp(article.get("datetime", 0)),
            "related_tickers": article.get("related", []),
        }

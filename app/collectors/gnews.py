"""GNews Collector (stub)."""
from typing import Any, Dict, List, Optional


class GNewsCollector:
    """GNews collector stub."""

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def get_company_news(
        self, symbol: str, from_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Fetch news from GNews."""
        # TODO: Implement GNews API
        return []

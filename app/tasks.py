"""Celery tasks for news collection."""
import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List
from celery import shared_task
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import AsyncSessionLocal
from app.models import Article, Company
from app.collectors.finnhub import FinnhubCollector

logger = logging.getLogger(__name__)
settings = get_settings()


@shared_task(bind=True)
async def collect_news_for_all_companies(self) -> Dict[str, Any]:
    """Collect news from Finnhub for all active companies."""
    async with AsyncSessionLocal() as session:
        try:
            companies_result = await session.execute(
                select(Company).where(Company.is_active == True)
            )
            companies = companies_result.scalars().all()

            if not companies:
                logger.warning("No active companies found")
                return {"status": "success", "message": "No companies", "count": 0}

            collector = FinnhubCollector(api_key=settings.finnhub_api_key)
            total_articles = 0

            for company in companies:
                from_date = (datetime.utcnow() - timedelta(hours=24)).strftime("%Y-%m-%d")
                to_date = datetime.utcnow().strftime("%Y-%m-%d")

                articles = await collector.get_company_news(
                    symbol=company.ticker,
                    from_date=from_date,
                    to_date=to_date,
                )

                if not articles:
                    logger.warning(f"No articles found for {company.ticker}")
                    continue

                added = await _add_articles_to_db(
                    session=session,
                    articles=articles,
                    company=company,
                )
                total_articles += added

                logger.info(f"Added {added} articles for {company.ticker}")

            return {
                "status": "success",
                "total_articles_added": total_articles,
                "companies_processed": len(companies),
            }
        except Exception as e:
            logger.exception(f"Error collecting news: {e}")
            return {"status": "error", "message": str(e)}


async def _add_articles_to_db(
    session: AsyncSession,
    articles: List[Dict[str, Any]],
    company: Company,
) -> int:
    """Add articles to database, skipping duplicates."""
    added_count = 0

    for article_data in articles:
        # Check for existing article by hash
        content_hash = Article.compute_hash(
            article_data["title"], article_data["url"]
        )

        existing_result = await session.execute(
            select(Article).filter_by(content_hash=content_hash)
        )
        existing = existing_result.scalar_one_or_none()

        if existing:
            continue

        # Create new article
        article = Article(
            title=article_data["title"],
            url=article_data["url"],
            source=article_data.get("source", "unknown"),
            content_hash=content_hash,
        )

        if article_data.get("description"):
            article.description = article_data["description"]
        if article_data.get("image"):
            article.image = article_data["image"]
        if article_data.get("content"):
            article.content = article_data["content"]
        if article_data.get("published_at"):
            article.published_at = article_data["published_at"]

        session.add(article)
        article.companies.append(company)
        added_count += 1

    await session.flush()
    return added_count


@shared_task(bind=True)
async def cleanup_old_articles(self) -> Dict[str, Any]:
    """Remove articles older than 90 days."""
    async with AsyncSessionLocal() as session:
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=90)
            result = await session.execute(
                select(Article).filter(Article.created_at < cutoff_date)
            )
            old_articles = result.scalars().all()

            deleted_count = len(old_articles)

            for article in old_articles:
                await session.delete(article)

            await session.commit()

            logger.info(f"Deleted {deleted_count} old articles")

            return {"status": "success", "deleted_count": deleted_count}
        except Exception as e:
            logger.exception(f"Error cleaning up articles: {e}")
            return {"status": "error", "message": str(e)}


@shared_task
async def collect_news_on_startup() -> None:
    """One-time news collection on application startup."""
    logger.info("Running initial news collection...")
    result = await collect_news_for_all_companies()
    logger.info(f"Initial collection completed: {result}")

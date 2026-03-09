"""Pydantic schemas for API responses."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ArticleBase(BaseModel):
    """Base article schema."""
    title: str = Field(..., description="Article title")
    url: str = Field(..., description="Article URL")
    source: str = Field(..., description="News source (finnhub, alphavantage, gnews)")
    description: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    published_at: Optional[datetime] = None


class ArticleResponse(ArticleBase):
    """Article with ID."""
    id: int = Field(..., description="Article ID")
    content_hash: str = Field(..., description="SHA-256 hash for deduplication")
    created_at: datetime = Field(..., description="Database creation timestamp")
    updated_at: datetime = Field(..., description="Database update timestamp")


class ArticleListResponse(BaseModel):
    """Paginated article list."""
    items: List[ArticleResponse] = Field(..., description="List of articles")
    total: int = Field(..., description="Total number of articles")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Items per page")
    total_pages: int = Field(..., description="Total number of pages")


class CompanyBase(BaseModel):
    """Base company schema."""
    ticker: str = Field(..., description="Stock ticker symbol")
    name: str = Field(..., description="Company name")
    sector: Optional[str] = None
    is_active: bool = True


class CompanyResponse(CompanyBase):
    """Company with ID."""
    id: int = Field(..., description="Company ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Update timestamp")


class CompanyInfoResponse(CompanyBase):
    """Company with article count."""
    article_count: int = Field(default=0, description="Number of articles for this company")

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import hashlib

Base = declarative_base()


article_companies = Table(
    "article_companies",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("articles.id", ondelete="CASCADE"), primary_key=True),
    Column("company_id", Integer, ForeignKey("companies.id", ondelete="CASCADE"), primary_key=True),
)


class Article(Base):
    """Stock news article with deduplication."""
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    url = Column(String(1000), unique=True, nullable=False, index=True)
    source = Column(String(50), nullable=False, index=True)
    description = Column(Text)
    content = Column(Text)
    image = Column(String(500))
    published_at = Column(DateTime, index=True)
    content_hash = Column(String(64), unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    companies = relationship("Company", secondary=article_companies, back_populates="articles")

    @staticmethod
    def compute_hash(title: str, url: str) -> str:
        """Compute SHA-256 hash for deduplication."""
        combined = f"{title}|{url}"
        return hashlib.sha256(combined.encode()).hexdigest()

    @classmethod
    def create_from_dict(cls, data: dict) -> "Article":
        """Create Article instance from normalized data dict."""
        return cls(
            title=data["title"],
            url=data["url"],
            source=data["source"],
            description=data.get("description"),
            content=data.get("content"),
            image=data.get("image"),
            published_at=data.get("published_at"),
            content_hash=cls.compute_hash(data["title"], data["url"]),
        )


class Company(Base):
    """Stock ticker information."""
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    sector = Column(String(100))
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    articles = relationship("Article", secondary=article_companies, back_populates="companies")


class ArticleSignal(Base):
    """Sentiment/relevance signals for articles (ready for future use)."""
    __tablename__ = "article_signals"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False, index=True)
    signal_type = Column(String(50), nullable=False)
    score = Column(Integer)  # Store as percentage (e.g., 75 for 0.75)
    created_at = Column(DateTime, default=datetime.utcnow)

    article = relationship("Article")

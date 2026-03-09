"""Test SQLAlchemy models."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Article


class TestArticleModel:
    """Tests for Article model."""

    def test_compute_content_hash(self):
        """Test hash computation."""
        hash1 = Article.compute_hash("Test Title", "https://example.com")

        assert len(hash1) == 64  # SHA-256 hex length

    def test_compute_hash_deterministic(self):
        """Test hash is deterministic."""
        hash1 = Article.compute_hash("Title", "https://example.com")
        hash2 = Article.compute_hash("Title", "https://example.com")
        hash3 = Article.compute_hash("Different", "https://example.com")

        assert hash1 == hash2
        assert hash1 != hash3

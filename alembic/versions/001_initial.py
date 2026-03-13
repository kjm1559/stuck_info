"""initial schema

Revision ID: 001_initial
Revises: 
Create Date: 2026-03-13

"""
from __future__ import annotations
from typing import Sequence, Set, Optional
import sqlalchemy as sa
from alembic import op


# Revision identifiers
revision: str = '001_initial'
down_revision: Optional[str] = None
branch_labels: Optional[Sequence[str]] = None
depends_on: Optional[Sequence[str]] = None


def upgrade() -> None:
    # Create companies table
    op.create_table(
        'companies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('ticker', sa.String(length=10), nullable=False),
        sa.Column('name', sa.String(length=200), nullable=False),
        sa.Column('sector', sa.String(length=100)),
        sa.Column('is_active', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_companies_id', 'companies', ['id'], unique=False)
    op.create_index('ix_companies_ticker', 'companies', ['ticker'], unique=True)

    # Create articles table
    op.create_table(
        'articles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('url', sa.String(length=1000), nullable=False),
        sa.Column('source', sa.String(length=50), nullable=False),
        sa.Column('description', sa.Text()),
        sa.Column('content', sa.Text()),
        sa.Column('image', sa.String(length=500)),
        sa.Column('published_at', sa.DateTime()),
        sa.Column('content_hash', sa.String(length=64), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_articles_id', 'articles', ['id'], unique=False)
    op.create_index('ix_articles_content_hash', 'articles', ['content_hash'], unique=True)
    op.create_index('ix_articles_published_at', 'articles', ['published_at'], unique=False)
    op.create_index('ix_articles_source', 'articles', ['source'], unique=False)
    op.create_index('ix_articles_title', 'articles', ['title'], unique=False)
    op.create_index('ix_articles_url', 'articles', ['url'], unique=True)

    # Create article_companies association table
    op.create_table(
        'article_companies',
        sa.Column('article_id', sa.Integer(), nullable=False),
        sa.Column('company_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('article_id', 'company_id'),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
    )

    # Create article_signals table
    op.create_table(
        'article_signals',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('article_id', sa.Integer(), nullable=False),
        sa.Column('signal_type', sa.String(length=50), nullable=False),
        sa.Column('score', sa.Integer()),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ondelete='CASCADE'),
    )
    op.create_index('ix_article_signals_article_id', 'article_signals', ['article_id'], unique=False)
    op.create_index('ix_article_signals_id', 'article_signals', ['id'], unique=False)


def downgrade() -> None:
    # Drop tables in reverse order
    op.drop_index('ix_article_signals_id', table_name='article_signals')
    op.drop_index('ix_article_signals_article_id', table_name='article_signals')
    op.drop_table('article_signals')
    
    op.drop_table('article_companies')
    
    op.drop_index('ix_articles_url', table_name='articles')
    op.drop_index('ix_articles_title', table_name='articles')
    op.drop_index('ix_articles_source', table_name='articles')
    op.drop_index('ix_articles_published_at', table_name='articles')
    op.drop_index('ix_articles_content_hash', table_name='articles')
    op.drop_index('ix_articles_id', table_name='articles')
    op.drop_table('articles')
    
    op.drop_index('ix_companies_ticker', table_name='companies')
    op.drop_index('ix_companies_id', table_name='companies')
    op.drop_table('companies')

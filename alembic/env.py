from logging.config import fileConfig
from sqlalchemy import pool, create_engine, Connection
from alembic import context
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

config = context.config

# Import models and config
try:
    from app.models import Base
    from app.config import get_settings
    
    settings = get_settings()
    if config.config_file_name is not None:
        config.set_main_option("sqlalchemy.url", settings.database_url)
        fileConfig(config.config_file_name)
    target_metadata = Base.metadata
except (ImportError, Exception) as e:
    print(f"Warning: Could not load models: {e}")
    target_metadata = None


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    engine = create_engine(
        config.get_main_option("sqlalchemy.url"),
        poolclass=pool.NullPool,
    )
    
    with engine.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()
    
    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

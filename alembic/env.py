from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from models import Base  # Ensure this import matches your project structure

# Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set the target metadata for 'autogenerate' support
target_metadata = Base.metadata


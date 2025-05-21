from sqlmodel import SQLModel
from alembic import context
from sqlalchemy import engine_from_config, pool
import os, sys

sys.path.append(os.getcwd())
from app.domain.entities import *          # importa todas las entidades SQLModel
from app.infrastructure.db.scripts import init_db  # opcional

config = context.config
target_metadata = SQLModel.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    context.run_migrations()
else:
    run_migrations_online()

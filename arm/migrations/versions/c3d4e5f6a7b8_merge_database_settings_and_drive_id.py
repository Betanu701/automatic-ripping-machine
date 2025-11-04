"""Merge multiple heads: database settings and drive_id branches

Revision ID: c3d4e5f6a7b8
Revises: a79af75f4b31, 469d88477c13
Create Date: 2025-11-04 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3d4e5f6a7b8'
down_revision = ('a79af75f4b31', '469d88477c13')
branch_labels = None
depends_on = None


def upgrade():
    """Merge migration - no schema changes needed."""
    pass


def downgrade():
    """Merge migration - no schema changes needed."""
    pass

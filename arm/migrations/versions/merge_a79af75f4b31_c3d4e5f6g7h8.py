"""Merge heads a79af75f4b31 and c3d4e5f6g7h8

Revision ID: m_merge_a79af75f_c3d4e5f
Revises: a79af75f4b31, c3d4e5f6g7h8
Create Date: 2025-10-19 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'm_merge_a79af75f_c3d4e5f'
down_revision = ('a79af75f4b31', 'c3d4e5f6g7h8')
branch_labels = None
depends_on = None


def upgrade():
    """No-op merge revision. This file merges two branch heads so Alembic
    has a single linear head. No schema changes are required here."""
    pass


def downgrade():
    """Downgrade is a no-op for merge-only revisions."""
    pass

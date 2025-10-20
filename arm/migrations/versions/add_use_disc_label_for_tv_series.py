"""Add USE_DISC_LABEL_FOR_TV_SERIES to config

Revision ID: add_use_disc_label_for_tv_series
Revises: 2986d3f7ecf9
Create Date: 2025-10-15 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_use_disc_label_for_tv_series'
down_revision = '2986d3f7ecf9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('config',
                  sa.Column('USE_DISC_LABEL_FOR_TV_SERIES', sa.Boolean(), nullable=True)
                  )


def downgrade():
    op.drop_column('config', 'USE_DISC_LABEL_FOR_TV_SERIES')
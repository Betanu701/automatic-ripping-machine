"""Merge config and batch_rename branches

Revision ID: f5g6h7i8j9k0
Revises: b2c3d4e5f6g7, d4e5f6g7h8i9
Create Date: 2025-01-14 10:30:00.000000

This merge resolves the multiple heads issue by combining:
1. b2c3d4e5f6g7 (config_add_group_tv_discs_under_series) 
2. d4e5f6g7h8i9 (merge_add_drive_id_and_batch_rename)

No schema changes are needed for this merge.
"""
# no imports required, for the merge of forked databases
# from alembic import op
# import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f5g6h7i8j9k0'
down_revision = ('b2c3d4e5f6g7', 'd4e5f6g7h8i9')
branch_labels = None
depends_on = None


def upgrade():
    """Merge two branches - no schema changes needed."""
    pass


def downgrade():
    """Merge two branches - no schema changes needed."""
    pass

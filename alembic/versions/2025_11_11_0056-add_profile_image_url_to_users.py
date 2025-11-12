"""Add profile_image_url to users

Revision ID: a1b2c3d4e5f6
Revises: 811c5bfc2482
Create Date: 2025-11-11 00:56:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '811c5bfc2482'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade database schema."""
    op.add_column('users', sa.Column('profile_image_url', sa.String(length=500), nullable=True))


def downgrade() -> None:
    """Downgrade database schema."""
    op.drop_column('users', 'profile_image_url')

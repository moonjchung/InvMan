"""add_average_cost_to_items

Revision ID: c9fed02566b0
Revises: 91e582922967
Create Date: 2025-08-29 13:14:16.128001

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9fed02566b0'
down_revision: Union[str, Sequence[str], None] = '91e582922967'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('items', sa.Column('average_cost', sa.Float(), nullable=True, server_default='0.0'))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('items', 'average_cost')

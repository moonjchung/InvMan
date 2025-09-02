"""add stock level and inventory transactions

Revision ID: b395bd7f15f5
Revises: eb258730cffb
Create Date: 2025-08-27 23:57:05.304838

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b395bd7f15f5'
down_revision: Union[str, Sequence[str], None] = 'eb258730cffb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('quantity', new_column_name='stock_level', existing_type=sa.INTEGER(), nullable=False)

    op.create_table('inventory_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('quantity_change', sa.Integer(), nullable=False),
        sa.Column('new_quantity', sa.Integer(), nullable=False),
        sa.Column('notes', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('items', schema=None) as batch_op:
        batch_op.alter_column('stock_level', new_column_name='quantity', existing_type=sa.INTEGER(), nullable=False)

    op.drop_table('inventory_transactions')

"""real coin migrations

Revision ID: 56786b2b4e1d
Revises: aa8479ee8ac2
Create Date: 2024-08-23 23:35:18.266428

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '56786b2b4e1d'
down_revision: Union[str, None] = 'aa8479ee8ac2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('coins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('market', sa.String(length=100), nullable=False),
    sa.Column('korean_name', sa.String(length=200), nullable=False),
    sa.Column('english_name', sa.String(length=200), nullable=False),
    sa.Column('market_event_warning', sa.Boolean(), nullable=False),
    sa.Column('market_event_caution', sa.JSON(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('english_name'),
    sa.UniqueConstraint('korean_name')
    )
    op.create_index(op.f('ix_coins_id'), 'coins', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_coins_id'), table_name='coins')
    op.drop_table('coins')
    # ### end Alembic commands ###

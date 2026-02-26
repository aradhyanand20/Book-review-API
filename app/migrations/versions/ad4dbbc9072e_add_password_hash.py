"""add password hash

Revision ID: ad4dbbc9072e
Revises: f83cd37424b6
Create Date: 2026-02-26 23:15:13.576820

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = 'ad4dbbc9072e'
down_revision: Union[str, Sequence[str], None] = 'f83cd37424b6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users',
        sa.Column('password_hash', sa.VARCHAR(), nullable=False, server_default='')
    )
    # remove server_default after migration if you don't want it permanently
    op.alter_column('users', 'password_hash', server_default=None)

def downgrade() -> None:
    op.drop_column('users', 'password_hash')
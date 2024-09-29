"""Add number field to Customer

Revision ID: 52863ab5f0fd
Revises: 
Create Date: 2024-09-25 12:14:08.394794

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52863ab5f0fd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Add the number column to the customers table
    op.add_column('customers', sa.Column('number', sa.String(), nullable=True))

def downgrade():
    # Remove the number column in case of downgrade
    op.drop_column('customers', 'number')
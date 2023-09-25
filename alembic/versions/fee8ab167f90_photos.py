"""Photos

Revision ID: fee8ab167f90
Revises: bfd0eed58182
Create Date: 2023-09-25 11:23:33.220780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fee8ab167f90'
down_revision: Union[str, None] = 'bfd0eed58182'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photo',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=500), nullable=False),
    sa.Column('id_owner', sa.Integer(), nullable=False),
    sa.Column('creation_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('modification_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['id_owner'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('photo')
    # ### end Alembic commands ###

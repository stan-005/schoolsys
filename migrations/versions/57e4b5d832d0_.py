"""empty message

Revision ID: 57e4b5d832d0
Revises: 62e1bd7aa2ce
Create Date: 2024-02-08 10:30:01.298317

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57e4b5d832d0'
down_revision = '62e1bd7aa2ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('grade1',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('grade1')
    # ### end Alembic commands ###

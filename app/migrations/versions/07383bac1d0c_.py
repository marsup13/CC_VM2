"""empty message

Revision ID: 07383bac1d0c
Revises: 4820461630c4
Create Date: 2021-11-21 12:44:08.619124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '07383bac1d0c'
down_revision = '4820461630c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('thread',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=30), nullable=True),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('thread')
    # ### end Alembic commands ###

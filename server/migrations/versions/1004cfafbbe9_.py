"""empty message

Revision ID: 1004cfafbbe9
Revises: 5155af63a133
Create Date: 2014-04-20 23:47:21.514625

"""

# revision identifiers, used by Alembic.
revision = '1004cfafbbe9'
down_revision = '5155af63a133'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('authors', sa.Column('date_created', sa.DateTime(), nullable=True))
    op.add_column('books', sa.Column('date_created', sa.DateTime(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('books', 'date_created')
    op.drop_column('authors', 'date_created')
    ### end Alembic commands ###

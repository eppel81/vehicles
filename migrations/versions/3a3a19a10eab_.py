"""empty message

Revision ID: 3a3a19a10eab
Revises: 12b3684e31e7
Create Date: 2015-11-24 09:24:29.027837

"""

# revision identifiers, used by Alembic.
revision = '3a3a19a10eab'
down_revision = '12b3684e31e7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('object2user', sa.Column('visible', sa.Boolean(), nullable=True))
    op.drop_column('object2user', 'txt')
    op.drop_column('object2user', 'locked')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('object2user', sa.Column('locked', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('object2user', sa.Column('txt', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('object2user', 'visible')
    ### end Alembic commands ###

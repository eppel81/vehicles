"""empty message

Revision ID: 3aa71ba32835
Revises: 16122df0465
Create Date: 2015-11-23 10:11:10.960839

"""

# revision identifiers, used by Alembic.
revision = '3aa71ba32835'
down_revision = '16122df0465'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('object2user', sa.Column('object_id', sa.Integer(), nullable=True))
    op.add_column('object2user', sa.Column('user_id', sa.Integer(), nullable=True))
    op.add_column('object2user', sa.Column('visible', sa.Boolean(), nullable=True))
    op.create_foreign_key(None, 'object2user', 'objects', ['object_id'], ['nid'])
    op.create_foreign_key(None, 'object2user', 'users', ['user_id'], ['nid'])
    op.drop_column('object2user', 'id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('object2user', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'object2user', type_='foreignkey')
    op.drop_constraint(None, 'object2user', type_='foreignkey')
    op.drop_column('object2user', 'visible')
    op.drop_column('object2user', 'user_id')
    op.drop_column('object2user', 'object_id')
    ### end Alembic commands ###

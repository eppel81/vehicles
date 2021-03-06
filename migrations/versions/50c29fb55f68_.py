"""empty message

Revision ID: 50c29fb55f68
Revises: 3a3a19a10eab
Create Date: 2015-11-24 10:51:26.797644

"""

# revision identifiers, used by Alembic.
revision = '50c29fb55f68'
down_revision = '3a3a19a10eab'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('object2user', sa.Column('object_id', sa.Integer(), nullable=False))
    op.add_column('object2user', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'object2user', 'objects', ['object_id'], ['nid'])
    op.create_foreign_key(None, 'object2user', 'users', ['user_id'], ['nid'])
    op.drop_column('object2user', 'id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('object2user', sa.Column('id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'object2user', type_='foreignkey')
    op.drop_constraint(None, 'object2user', type_='foreignkey')
    op.drop_column('object2user', 'user_id')
    op.drop_column('object2user', 'object_id')
    ### end Alembic commands ###

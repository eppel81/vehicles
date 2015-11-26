"""empty message

Revision ID: 18b470965629
Revises: 3aa71ba32835
Create Date: 2015-11-24 09:08:22.291876

"""

# revision identifiers, used by Alembic.
revision = '18b470965629'
down_revision = '3aa71ba32835'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('object2user', sa.Column('id', sa.Integer(), nullable=False))
    op.drop_constraint(u'object2user_user_id_fkey', 'object2user', type_='foreignkey')
    op.drop_constraint(u'object2user_object_id_fkey', 'object2user', type_='foreignkey')
    op.drop_column('object2user', 'visible')
    op.drop_column('object2user', 'user_id')
    op.drop_column('object2user', 'object_id')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('object2user', sa.Column('object_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('object2user', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('object2user', sa.Column('visible', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.create_foreign_key(u'object2user_object_id_fkey', 'object2user', 'objects', ['object_id'], ['nid'])
    op.create_foreign_key(u'object2user_user_id_fkey', 'object2user', 'users', ['user_id'], ['nid'])
    op.drop_column('object2user', 'id')
    ### end Alembic commands ###

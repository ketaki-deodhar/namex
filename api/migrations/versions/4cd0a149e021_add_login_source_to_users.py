"""add_login_source_to_users

Revision ID: 4cd0a149e021
Revises: 9d5d703de794
Create Date: 2022-11-24 11:11:23.358491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4cd0a149e021'
down_revision = '9d5d703de794'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('login_source', sa.String(length=200)))


def downgrade():
    op.drop_column('users', 'login_source')

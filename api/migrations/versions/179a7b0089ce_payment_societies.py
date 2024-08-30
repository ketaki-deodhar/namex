"""payment-societies

Revision ID: 179a7b0089ce
Revises: 6be595afb9ba
Create Date: 2024-08-27 16:45:02.229938

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '179a7b0089ce'
down_revision = '6be595afb9ba'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust!! ###
    op.create_table('payment_societies',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nr_num', sa.String(length=10), nullable=True),
    sa.Column('corp_num', sa.String(20), nullable=True),
    sa.Column('request_state', sa.String(length=40), nullable=True),
    sa.Column('payment_status', sa.String(length=50), nullable=True),
    sa.Column('payment_date', sa.DateTime(), nullable=True),    
    sa.Column('payment_json', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.ForeignKeyConstraint(['nr_id'], ['requests.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment_societies')
    # ### end Alembic commands ###    

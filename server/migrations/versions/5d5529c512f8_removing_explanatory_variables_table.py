"""removing explanatory variables table

Revision ID: 5d5529c512f8
Revises: 27cde118cb7b
Create Date: 2025-02-06 11:39:47.837458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d5529c512f8'
down_revision = '27cde118cb7b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('explanatory_variables')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('explanatory_variables',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('variable_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('data_type', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('is_explanatory', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=200), autoincrement=False, nullable=True),
    sa.Column('source_table', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='explanatory_variables_pkey')
    )
    # ### end Alembic commands ###

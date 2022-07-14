"""init

Revision ID: 804d794a4ecb
Revises: 
Create Date: 2022-07-14 17:38:50.417487

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '804d794a4ecb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timers',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('event', sa.Integer(), server_default='1', nullable=False),
    sa.Column('timestamp', sa.DateTime(), server_default=sa.text('current_timestamp'), nullable=True),
    sa.Column('timer', sa.Time(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timers')
    # ### end Alembic commands ###
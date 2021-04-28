"""add_is_ignored_column_to_channel_user

Revision ID: f9d5ee503852
Revises: 896109adc784
Create Date: 2021-04-28 21:56:11.774400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9d5ee503852'
down_revision = '896109adc784'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('channel_user', sa.Column('is_ignored', sa.Boolean(), server_default=sa.text('0'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('channel_user', 'is_ignored')
    # ### end Alembic commands ###

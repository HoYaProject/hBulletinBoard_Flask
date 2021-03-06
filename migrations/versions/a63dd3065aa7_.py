"""empty message

Revision ID: a63dd3065aa7
Revises: eb497edfb2b3
Create Date: 2021-02-13 15:38:32.759657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a63dd3065aa7'
down_revision = 'eb497edfb2b3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_model', schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f('uq_user_model_email'), ['email'])
        batch_op.create_unique_constraint(batch_op.f('uq_user_model_username'), ['username'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_model', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_model_username'), type_='unique')
        batch_op.drop_constraint(batch_op.f('uq_user_model_email'), type_='unique')

    # ### end Alembic commands ###

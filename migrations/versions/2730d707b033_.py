"""empty message

Revision ID: 2730d707b033
Revises: 42f7e1c260b7
Create Date: 2021-02-20 22:49:57.794726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2730d707b033'
down_revision = '42f7e1c260b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question_model', schema=None) as batch_op:
        batch_op.add_column(sa.Column('category', sa.String(length=16), server_default='qna', nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('question_model', schema=None) as batch_op:
        batch_op.drop_column('category')

    # ### end Alembic commands ###

"""empty message

Revision ID: 3329b91e4cc8
Revises: f0c184ea5bed
Create Date: 2022-08-24 18:29:23.626794

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3329b91e4cc8'
down_revision = 'f0c184ea5bed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('email', table_name='emailcpatcha')
    op.drop_table('emailcpatcha')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('emailcpatcha',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('email', mysql.VARCHAR(length=100), nullable=False),
    sa.Column('captcha', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('create_time', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_index('email', 'emailcpatcha', ['email'], unique=False)
    # ### end Alembic commands ###
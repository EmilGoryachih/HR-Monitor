"""

Revision ID: 3c7c474a819a
Revises: bcede4aace28
Create Date: 2024-10-05 16:15:54.637196

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c7c474a819a'
down_revision: Union[str, None] = 'bcede4aace28'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # Удалите или закомментируйте создание типа ENUM, если он уже существует.
    # op.create_enum('busyness', ['FULL', 'PARTIAL', 'PROJECT', 'VOLUNTEERING', 'INTERNSHIP', 'GPH'])

    op.create_table('resumes',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('study', sa.JSON(), nullable=True),
    sa.Column('desired_busyness', sa.ARRAY(sa.Enum('FULL', 'PARTIAL', 'PROJECT', 'VOLUNTEERING', 'INTERNSHIP', 'GPH', name='busyness')), nullable=True),
    sa.Column('specialization', sa.ARRAY(sa.String(length=50)), nullable=True),
    sa.Column('skills', sa.ARRAY(sa.String(length=20)), nullable=True),
    sa.Column('about_me', sa.String(length=1000), nullable=True),
    sa.Column('courses', sa.JSON(), nullable=True),
    sa.Column('work_experience', sa.ARRAY(sa.JSON()), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resumes_id'), 'resumes', ['id'], unique=False)
    op.create_index(op.f('ix_resumes_name'), 'resumes', ['name'], unique=False)
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_resumes_name'), table_name='resumes')
    op.drop_index(op.f('ix_resumes_id'), table_name='resumes')
    op.drop_table('resumes')
    # ### end Alembic commands ###

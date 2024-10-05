"""

Revision ID: b90aa8e1baee
Revises: fa4e89474a31
Create Date: 2024-10-05 17:23:45.823339

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b90aa8e1baee'
down_revision: Union[str, None] = 'fa4e89474a31'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('vacancy_user_association', sa.Column('ResumeId', sa.UUID(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('vacancy_user_association', 'ResumeId')
    # ### end Alembic commands ###

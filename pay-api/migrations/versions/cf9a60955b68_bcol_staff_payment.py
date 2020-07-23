"""bcol_staff_payment

Revision ID: cf9a60955b68
Revises: e8edc889072d
Create Date: 2020-07-21 08:52:47.896765

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf9a60955b68'
down_revision = 'e8edc889072d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('corp_type', sa.Column('bcol_staff_fee_code', sa.String(length=20), nullable=True))
    op.add_column('invoice', sa.Column('dat_number', sa.String(length=50), nullable=True))
    op.create_index(op.f('ix_invoice_dat_number'), 'invoice', ['dat_number'], unique=False)
    op.execute('update corp_type set bcol_staff_fee_code=\'CBCOMVC1\' where code=\'BC\'')
    op.execute('update corp_type set bcol_staff_fee_code=\'COOPVC01\' where code=\'CP\'')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_invoice_dat_number'), table_name='invoice')
    op.drop_column('invoice', 'dat_number')
    op.drop_column('corp_type', 'bcol_staff_fee_code')
    # ### end Alembic commands ###

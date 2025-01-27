from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = 'dad2547c703b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """# ### commands auto generated by Alembic - please adjust."""
    op.create_table(
        'administration_user',
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment='Номер в базе данных',
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('administration_user', schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f('ix_administration_user_email'), ['email'], unique=True
        )

    op.create_table(
        'category',
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment='Номер в базе данных',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'maker',
        sa.Column('logo', sa.String(), nullable=False, comment='logo link'),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment='Номер в базе данных',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('logo'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'parameter',
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment='Номер в базе данных',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
    )
    op.create_table(
        'user',
        sa.Column(
            'tg_username',
            sa.String(),
            nullable=False,
            comment='Username пользователя в Telegram',
        ),
        sa.Column(
            'tg_chat_id',
            sa.BigInteger(),
            nullable=False,
            comment='Идентификатор чата с пользователем в Telegram',
        ),
        sa.Column(
            'name', sa.String(), nullable=True, comment='Имя пользователя'
        ),
        sa.Column(
            'phone_number',
            sa.String(),
            nullable=True,
            comment='Контактный номер телефона пользователя',
        ),
        sa.Column(
            'email',
            sa.String(),
            nullable=True,
            comment='Контактный email-адрес пользователя',
        ),
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment='Номер в базе данных',
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tg_chat_id'),
        sa.UniqueConstraint('tg_username'),
    )
    op.create_table(
        'equipment',
        sa.Column(
            'equipment_picture',
            sa.String(),
            nullable=True,
            comment='picture link',
        ),
        sa.Column(
            'maker_id',
            sa.Integer(),
            nullable=False,
            comment='relationship maker model',
        ),
        sa.Column(
            'category_id',
            sa.Integer(),
            nullable=False,
            comment='relationship category model',
        ),
        sa.Column(
            'pdf_catalog', sa.String(), nullable=False, comment='pdf link'
        ),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment='Номер в базе данных',
        ),
        sa.ForeignKeyConstraint(
            ['category_id'],
            ['category.id'],
        ),
        sa.ForeignKeyConstraint(
            ['maker_id'],
            ['maker.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('pdf_catalog'),
    )
    op.create_table(
        'equipmentparameter',
        sa.Column(
            'equipment_id',
            sa.Integer(),
            nullable=False,
            comment='relationship equipment model',
        ),
        sa.Column(
            'parameter_id',
            sa.Integer(),
            nullable=False,
            comment='relationship parameter model',
        ),
        sa.Column(
            'id',
            sa.Integer(),
            autoincrement=True,
            nullable=False,
            comment='Номер в базе данных',
        ),
        sa.ForeignKeyConstraint(
            ['equipment_id'],
            ['equipment.id'],
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        sa.ForeignKeyConstraint(
            ['parameter_id'],
            ['parameter.id'],
            onupdate='CASCADE',
            ondelete='CASCADE',
        ),
        sa.PrimaryKeyConstraint('equipment_id', 'parameter_id', 'id'),
        sa.UniqueConstraint(
            'equipment_id',
            'parameter_id',
            name='idx_unique_equipment_parameter',
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """# ### commands auto generated by Alembic - please adjust."""
    op.drop_table('equipmentparameter')
    op.drop_table('equipment')
    op.drop_table('user')
    op.drop_table('parameter')
    op.drop_table('maker')
    op.drop_table('category')
    with op.batch_alter_table('administration_user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_administration_user_email'))

    op.drop_table('administration_user')
    # ### end Alembic commands ###

"""Base tables

Revision ID: 1d6f0a8d0ee7
Revises: 
Create Date: 2023-05-10 00:15:30.925674

"""
from enum import Enum
from datetime import datetime as dt

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1d6f0a8d0ee7'
down_revision = None
branch_labels = None
depends_on = None


class MeasureUnits(str, Enum):
    PIECES = 'pieces'
    GRAMS = 'grams'
    MILLILITERS = 'milliliters'
    PINCH = 'pinch'
    SPOONS = 'spoons'


def upgrade() -> None:

    op.create_table(
        'ingredient',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String),
        sa.Column('measure_unit', sa.Enum(MeasureUnits)),
        sa.Column('amount', sa.Float),
    )

    op.create_table(
        'recipe',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('title', sa.String),
        sa.Column('description', sa.String),
        sa.Column('created_at', sa.DateTime, default=dt.now),
        sa.Column('updated_at', sa.DateTime, nullable=True),
    )

    op.create_table(
        'recipe_step',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('order', sa.Integer),
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipe.id')),
        sa.Column('description', sa.String),
    )

    op.create_table(
        'recipe_to_ingredient',
        sa.Column('recipe_id', sa.Integer, sa.ForeignKey('recipe.id')),
        sa.Column('ingredient_id', sa.Integer, sa.ForeignKey('ingredient.id'))
    )

def downgrade() -> None:
    op.drop_table('recipe_to_ingredient')
    op.drop_table('ingredient')
    op.drop_table('recipe_step')
    op.drop_table('recipe')


import asyncio
from enum import Enum

from datetime import datetime as dt

from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    Float,
    DateTime,
    ForeignKey,
    Enum as saEnum,
)
from sqlalchemy.orm import relationship

from app.core.db import Base, engine


class MeasureUnits(str, Enum):
    PIECES = 'pieces'
    GRAMS = 'grams'
    MILLILITERS = 'milliliters'
    PINCH = 'pinch'
    SPOONS = 'spoons'



recipe_to_ingredient = Table(
    'recipe_to_ingredient',
    Base.metadata,
    Column('recipe_id', ForeignKey('recipe.id')),
    Column('ingredient_id', ForeignKey('ingredient.id')),
)


class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True, autoincrement=True,)
    title = Column(String)
    measure_unit = Column(saEnum(MeasureUnits))
    amount = Column(Float)
    Recipe = relationship(
        'Recipe',
        secondary=recipe_to_ingredient,
        back_populates='ingredients',
    )

class RecipeStep(Base):
    __tablename__ = 'recipe_step'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order = Column(Integer)
    recipe_id = Column(Integer, ForeignKey('recipe.id'))
    description = Column(String)
    recipe = relationship('Recipe', back_populates='steps')


class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    steps = relationship('RecipeStep')
    ingredients = relationship(
        'Ingredient',
        secondary=recipe_to_ingredient,
        back_populates='recipes',
    )
    created_at = Column(DateTime, default=dt.now)
    updated_at = Column(DateTime, nullable=True)


async def create_models():
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(create_models())
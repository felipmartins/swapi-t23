from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class PlanetBase(SQLModel):

    name: str = Field(max_length=100)
    rotation_period: str = Field(max_length=40)
    orbital_period: str = Field(max_length=40)
    diameter: str = Field(max_length=40)
    climate: str = Field(max_length=40)
    gravity: str = Field(max_length=40)
    terrain: str = Field(max_length=40)
    surface_water: str = Field(max_length=40)
    population: str = Field(max_length=40)


class Planet(PlanetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    residents: List["People"] = Relationship(back_populates="homeworld")


class PlanetCreate(PlanetBase):
    pass


class PlanetRead(PlanetBase):
    id: int
    residents: List["People"] = []


class People(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str = Field(max_length=100)
    height: str = Field(max_length=50)
    mass: str = Field(max_length=50)
    hair_color: str = Field(max_length=50)
    skin_color: str = Field(max_length=50)
    eye_color: str = Field(max_length=50)
    birth_year: str = Field(max_length=50)
    gender: str = Field(max_length=50)

    planet_id: int = Field(default=None, foreign_key="planet.id")
    homeworld: Planet = Relationship(back_populates="residents")


PlanetRead.update_forward_refs()
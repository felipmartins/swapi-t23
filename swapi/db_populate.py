import json
from sqlmodel import select
from swapi.model import Planet, People


def is_table_empty(session, model):
    return session.exec(select(model)).first() is None


def populate_empty_tables(session):

    if is_table_empty(session, Planet):
        populate_table_planet(session)

    if is_table_empty(session, People):
        populate_table_people(session)


def populate_table_planet(session):

    with open("data/planets.json") as file:
        planets = json.load(file)
    
    for each_planet in planets:
        planet = Planet(**each_planet)

        session.add(planet)
        session.commit()


def populate_table_people(session):

    with open("data/people.json") as file:
        people = json.load(file)
    
    for each_person in people:
        person = People(**each_person)

        session.add(person)
        session.commit()
from fastapi import FastAPI
from sqlmodel import Session, select
from swapi.model import Planet, People, PlanetRead, PlanetCreate
from swapi.db import create_db_and_tables, engine
from swapi.db_populate import populate_empty_tables
from fastapi.middleware.cors import CORSMiddleware

origins = ["http://localhost:3000",]


app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)


def get_session():
    return Session(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

    with get_session() as session:
        populate_empty_tables(session)


def create_response(result):
  return {
      "count": len(result),
      "next": None,
      "previous": None,
      "results": result,
  }


@app.get('/')
async def hello_world():
    return {"details":"Hello T23!!!!!"}


@app.get("/api/people/", tags=["people"])
async def list_people():
  with get_session() as session:
      people = session.exec(select(People)).all()
      return create_response(people)


@app.get("/api/planets/", tags=["planets"])
async def list_planets():
  with get_session() as session:
      planets = session.exec(select(Planet)).all()
      return create_response(planets)


@app.post("/api/planets/", tags=["planets"], status_code=201)
async def create_planet(planet: PlanetCreate):
   with get_session() as session:
      db_planet = Planet.from_orm(planet)
      session.add(db_planet)
      session.commit()
      session.refresh(db_planet)
      return db_planet
   

@app.get("/api/planets/{id}", tags=["planets"], response_model=PlanetRead)
async def get_planet_by_id(id: int):
   with get_session() as session:
      result = session.exec(select(Planet).where(Planet.id  == id)).one()
      result.residents #due to lazy loading
      return result

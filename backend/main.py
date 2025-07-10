from fastapi import FastAPI

from app.database import Base, engine
from app.routes import note, register, login


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Note-taking App API",
    description="This is a structure for a Note-taking App"
)

app.include_router(note.route)
app.include_router(register.route)
app.include_router(login.route)
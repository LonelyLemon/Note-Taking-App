from fastapi import FastAPI

from src.database import Base, engine
from src.routes import note, register, login, user, logout


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Note-taking App API",
    description="This is a structure for a Note-taking App"
)

app.include_router(note.route)
app.include_router(register.route)
app.include_router(login.route)
app.include_router(user.route)
app.include_router(logout.route)
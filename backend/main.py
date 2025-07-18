from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database import Base, engine
from src.routes import note, register, login, user, logout


# Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Note-taking App API",
    description="This is a structure for a Note-taking App"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def init_fnc():
    async with engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

app.include_router(note.route)
app.include_router(register.route)
app.include_router(login.route)
app.include_router(user.route)
app.include_router(logout.route)
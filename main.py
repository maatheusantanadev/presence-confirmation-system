from fastapi import FastAPI
from Database.database import engine, Base
from Routes import students, users, presences

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(students.router)
app.include_router(users.router)
app.include_router(presences.router)

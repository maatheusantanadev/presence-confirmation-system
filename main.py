from fastapi import FastAPI
from Database.database import engine, Base
from Routes import students, users, presences, groups, stats
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)
app.include_router(users.router)
app.include_router(presences.router)
app.include_router(groups.router)
app.include_router(stats.router)

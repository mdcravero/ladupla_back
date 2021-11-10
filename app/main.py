from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
import models
from db.conexion import *
from routes.auth import auth
from routes.bookings import booking
from routes.users import user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title='test FastAPI',
              description='Backend App La Dupla',
              version='1.0')

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth)
app.include_router(user)
app.include_router(booking)


@app.get("/", tags=['Documentation'])
def main():
    return RedirectResponse(url="/docs/")

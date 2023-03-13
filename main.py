from fastapi import FastAPI
from routers import animal_api

app = FastAPI()
app.include_router(animal_api.router)

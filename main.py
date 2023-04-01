from fastapi import FastAPI
from Backend.api.routers import animal_api
from Frontend.Routers import back_to_front

app = FastAPI()
app.include_router(animal_api.router)
app.include_router(back_to_front.router)

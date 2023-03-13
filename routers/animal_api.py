from fastapi import APIRouter, HTTPException, status
from db.models.animal import Animal
from db.models.race import Race
from db.client_db import client_db
from bson import ObjectId
from db.schemas.animal import animal_schema, animals_schema

router = APIRouter(prefix="/animals",
                   tags=["animals"],
                   responses={
                       status.HTTP_404_NOT_FOUND: {
                           "message": "No se encuentra la ruta"
                       }
                   })

@router.get("/", response_model=list[Animal])
async def get_animals():
    return animals_schema(client_db.local.animals.find())

@router.get("/{id}")
async def get_animal(id: str):
    return search_animal("_id", ObjectId(id))

@router.post("/", response_model=Animal, status_code=status.HTTP_201_CREATED)
async def create_animal(animal: Animal):
    """Para comparar el animal para crear con alguno que pueda estar en la BD, lo buscamos, 
    les quitamos el ID a los dos y lo comparamos enteros."""
    new_animal = dict(animal)
    
    del new_animal["id"]
    new_animal["race"] = str(new_animal["race"].value)
    new_animal["sex"] = str(new_animal["sex"].value)
    
    searched_animal = dict(search_animal("name", animal.name))
    
    if type(search_animal("name", animal.name)) == Animal:
        searched_animal["race"] = str(searched_animal["race"].value)
        searched_animal["sex"] = str(searched_animal["sex"].value)
        del searched_animal["id"]
    
        if is_animal_equal(new_animal, searched_animal):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Este animal ya está registrado"
            )
        
    id = client_db.local.animals.insert_one(new_animal).inserted_id
    new_animal = animal_schema(client_db.local.animals.find_one({"_id":id}))
    
    return Animal(**new_animal)

def search_animal(field: str, key):
    try:
        animal = client_db.local.animals.find_one({field: key})
        return Animal(**animal_schema(animal))
    except:
        return {"error": "No se ha encontrado el animal"}

def is_animal_equal(animal1, animal2):
    if animal1["name"] == animal2["name"] and animal1["race"] == animal2["race"] and animal1["sex"] == animal2["sex"] and animal1["birth_date"] == animal2["birth_date"]:
        return True
    else:
        return False
from fastapi import APIRouter, HTTPException, status
from Backend.api.db.models.animal import Animal
from Backend.api.db.models.race import Race
from Backend.api.db.client_db import client_db
from bson import ObjectId
from Backend.api.db.schemas.animal import animal_schema, animals_schema

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
    
# Modify an animal in the database with the ID and the new data.
@router.put("/{id}", response_model=Animal, status_code=status.HTTP_201_CREATED)
async def modify_animal(id: str, animal: Animal):
    
    # Modify the animal object to be able to insert it in the database:
    animal_dict = dict(animal)
    animal_dict["race"] = str(animal_dict["race"].value)
    animal_dict["sex"] = str(animal_dict["sex"].value)
    del animal_dict["id"]
    
    # Check if the ID is valid:
    if not ObjectId.is_valid(id):
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f'ID {id} is not a valid id.'
            )
    
    animal_found = search_animal("_id", ObjectId(id))
    
    # Check if the animal has been found:
    if not isinstance(animal_found, Animal):
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f'Animal with ID {id} not found.'
            )
    # Find and animal with the given ID and replace de object animal found on the database:
    client_db.local.animals.replace_one({"_id": ObjectId(id)}, animal_dict)
    
    # Check if the animal has been modified:
    return search_animal("_id", ObjectId(id))
    
# Delete in the database the animal with the given ID.
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_animal(id: str):
    
    if not ObjectId.is_valid(id):
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f'ID {id} is not a valid id.'
            )
    
    searched_animal = search_animal("_id", ObjectId(id))
    if not isinstance(searched_animal, Animal):
        raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f'Animal with ID {id} not found.'
            )
    try:
        client_db.local.animals.delete_one({"_id": ObjectId(id)})
        return {"message": f"Animal with ID {id} deleted"}
    except:
        return {"error": "No se ha encontrado el animal"}
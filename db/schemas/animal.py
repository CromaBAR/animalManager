from db.models.race import Race, Sex


def animal_schema(animal) -> dict:
    
    return{
        "id": str(animal["_id"]),
        "name": animal["name"],
        "race": Race(animal["race"]),
        "sex": Sex(animal["sex"]),
        "description": animal["description"],
        "birth_date": animal["birth_date"]
    }
    
def animals_schema(animals) -> list:
    return [animal_schema(animal) for animal in animals]
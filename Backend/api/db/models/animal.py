from dataclasses import dataclass
from db.models.race import Race, Sex
from datetime import datetime
from pydantic import BaseModel
#from typing import Optional

#@dataclass
class Animal(BaseModel):
    """ Model class for a generic animal """
    id: str | None
    name: str
    race: Race
    sex: Sex
    description: str
    birth_date: datetime
    """
    @classmethod
    def __eq__(self, other_animal):
        if self.name == other_animal["name"] and self.race == other_animal["race"] and self.sex == other_animal["sex"] and self.birth_date == other_animal["birth_date"]:
            return True
        else:
            return False
    """
        

    
    
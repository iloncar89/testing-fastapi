from typing import Optional
from pydantic import BaseModel


class Person(BaseModel):
    id: Optional[int]
    first_name: str
    last_name: str
    year_of_birth: int

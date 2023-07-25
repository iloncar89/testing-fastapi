from pydantic import BaseModel


class PersonRequest(BaseModel):
    first_name: str
    last_name: str
    year_of_birth: int

class PersonResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    year_of_birth: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        
class GreetingRequest(BaseModel):
    name: str
    
class GreetingResponse(BaseModel):
    greeting: str
    
class CalculateFibonacciResponse(BaseModel):
    number: int

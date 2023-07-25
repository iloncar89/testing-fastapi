from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dependency_injector.wiring import inject, Provide

from config.containters import Container
from service.testService import TestService
from domain.person import Person
from model.person import Person as PersonModel
from payload.schemas import PersonRequest, PersonResponse, GreetingRequest, GreetingResponse, CalculateFibonacciResponse
import utils.appConstants as Constants

router = APIRouter(prefix="/api/v1/test")


@router.get("/case1")
async def hello():
    json_response = jsonable_encoder(GreetingResponse(greeting=Constants.HELLO))
    return JSONResponse(content=json_response)


@router.post("/case2")
async def greeting(payload: GreetingRequest):
    json_response = jsonable_encoder(GreetingResponse(greeting=Constants.HELLO + " " + payload.name))
    return JSONResponse(content=json_response)


@router.get("/case3/{number}")
@inject
async def calculate_fibonacci(
        number: int,
        test_service: TestService = Depends(Provide[Container.test_service]),
):
    try:
        calculation_result = test_service.calculate_fibonacci(number)
        
        json_response = jsonable_encoder(CalculateFibonacciResponse(number=calculation_result))
        return JSONResponse(content=json_response)
    except InterruptedError:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post("/case4")
@inject
async def create_get_delete_person_test_case(
        payload: PersonRequest,
        test_service: TestService = Depends(Provide[Container.test_service]),
):
    person = PersonModel(**payload.dict())
    
    person = test_service.create_get_delete_person_test_case(person)
    
    person_response = jsonable_encoder(PersonResponse(id=person.id, first_name=person.first_name, last_name=person.last_name,
                                     year_of_birth=person.year_of_birth))
    return JSONResponse(content=person_response)


@router.post("/case5")
@inject
async def create_get_delete_person_orm_test_case(
        payload: PersonRequest,
        test_service: TestService = Depends(Provide[Container.test_service]),
):
    person = Person(**payload.dict())
    
    person = test_service.create_get_delete_person_orm_test_case(person)
    
    person_response = jsonable_encoder(PersonResponse(id=person.id, first_name=person.first_name, last_name=person.last_name,
                                     year_of_birth=person.year_of_birth))
    return JSONResponse(content=person_response)

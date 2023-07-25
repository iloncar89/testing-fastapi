from dao.testDao import TestDao
from model.person import Person as PersonModel
from domain.person import Person


class TestService:
    def __init__(self, test_dao: TestDao):
        self._dao: TestDao = test_dao

    def calculate_fibonacci(self, number: int):
        if number <= 1:
            return number
        return self.calculate_fibonacci(number - 1) + self.calculate_fibonacci(number - 2)

    def create_get_delete_person_test_case(self, person: PersonModel) -> PersonModel:
        person.id = self._dao.add_person(person)
        person = self._dao.get_person_by_id(person.id)
        self._dao.delete_person_by_id(person.id)
        return person

    def create_get_delete_person_orm_test_case(self, person: Person) -> Person:
        person.id = self._dao.add_orm(person.first_name, person.last_name, person.year_of_birth)
        person = self._dao.get_by_id_orm(person.id)
        self._dao.delete_by_id_orm(person)
        return person

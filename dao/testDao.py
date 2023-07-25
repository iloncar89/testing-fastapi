from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from config.databaseDriver import DatabaseDriver
from model.person import Person as PersonModel

from domain.person import Person


class TestDao:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
        self.db_driver = DatabaseDriver()
        self.db_driver.connect()

    def add_person(self, person: PersonModel):
        create_user_query = """
        INSERT INTO person (first_name, last_name, year_of_birth) VALUES (%s, %s, %s) returning id;
        """

        cursor = self.db_driver.connection.cursor()
        data = (person.first_name, person.last_name, person.year_of_birth)

        try:
            cursor.execute(create_user_query, data)
            person.id = cursor.fetchone()[0]
            self.db_driver.connection.commit()
        except Exception as err:
            return {"error": err}
        else:
            return person.id
        finally:
            cursor.close()

    def get_person_by_id(self, person_id) -> PersonModel:
        get_user_by_id_query = """
        SELECT id, first_name, last_name, year_of_birth FROM person WHERE id = %s;
        """

        cursor = self.db_driver.connection.cursor()

        try:
            cursor.execute(get_user_by_id_query, (person_id,))
            record = cursor.fetchone()
            person = Person(id=record[0], first_name=record[1], last_name=record[2], year_of_birth=record[3])
            self.db_driver.connection.commit()
        except Exception as err:
            return {"error": err}
        else:
            return person
        finally:
            cursor.close()

    def delete_person_by_id(self, person_id):
        delete_person_by_id_query = """
        DELETE FROM person WHERE id=%s;
        """

        cursor = self.db_driver.connection.cursor()

        try:
            cursor.execute(delete_person_by_id_query, (person_id,))
            self.db_driver.connection.commit()
        except Exception as err:
            return {"error": err}
        else:
            return
        finally:
            cursor.close()

    def add_orm(self, name: str, surname: str, year: int) -> Person:
        with self.session_factory() as session:
            person = Person(first_name=name, last_name=surname, year_of_birth=year)
            session.add(person)
            session.commit()
            session.refresh(person)
            return person.id

    def get_by_id_orm(self, person_id: int) -> Person:
        with self.session_factory() as session:
            person = session.query(Person).filter(Person.id == person_id).first()
            if not person:
                raise UserNotFoundError(person_id)
            return person

    def delete_by_id_orm(self, person: Person):
        with self.session_factory() as session:
            session.delete(person)
            session.commit()
            return


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f"{self.entity_name} not found, id: {entity_id}")


class UserNotFoundError(NotFoundError):
    entity_name: str = "User"

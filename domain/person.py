from sqlalchemy import Column, String, Boolean, Integer

from config.databaseORM import Base


class Person(Base):

    __tablename__ = "person"

    id = Column('id', Integer, primary_key=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    year_of_birth = Column(Integer)

    def __repr__(self):
        return f"<Person(id={self.id}, " \
               f"first_name=\"{self.first_name}\", " \
               f"last_name=\"{self.last_name}\", " \
               f"year_of_birth={self.year_of_birth})>"
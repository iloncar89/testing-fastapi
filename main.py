from fastapi import FastAPI
from config import containters
from controller import testController


def create_app() -> FastAPI:
    containter = containters.Container()
    db = containter.dbORM()
    db.create_database()

    app = FastAPI()
    app.container = containter
    app.include_router(testController.router)
    return app


app = create_app()

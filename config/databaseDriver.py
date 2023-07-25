import psycopg2
import traceback
import sys
from psycopg2 import Error
from dependency_injector import providers


class DatabaseDriver:
    def __init__(self):
        self.connection = None

    def connect(self):
        # config = providers.Configuration(yaml_files=["config.yml"])
        try:
            self.connection = psycopg2.connect(
                user="postgres",
                password="testpass",
                database="postgres",
                host="postgres",
                port="5432"
            )

        except Exception as err:
            traceback.print_exc()
            error_str = "Error while connecing to DB : " + \
                        str(err)
            sys.exit(error_str)

    def shutdown(self):
        self.connection.close()

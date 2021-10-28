from typing import List

import psycopg2 as psycopg2

from DBConnections.db_config import DbConfig
from Repositories.db_connection import DbConnection


class PostgresDbConnection(DbConnection):
    def __init__(self, db_config: DbConfig):
        self.__conn = psycopg2.connect(**db_config.dict())

    def execute(self, sql) -> List:
        cursor = self.__conn.cursor()
        cursor.execute(sql)

        try:
            return cursor.fetchall()
        except psycopg2.ProgrammingError:
            return []

    def commit(self) -> None:
        self.__conn.commit()

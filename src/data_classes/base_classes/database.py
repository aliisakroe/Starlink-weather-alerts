''' 2 classes: NOAA MagnetosphereDB and NOAA PlasmaDB implement Database'''

import abc
import sqlite3 as sl

class Database(abc.ABC):
    '''Abstract class for storing api data
    must define table schema and multiple inserts
    '''

    def __init__(self, db, table):
        self.name = table
        self.db = db
        self._open_connection()

    def get_table_name(self):
        return self.name

    def get_db_name(self):
        return self.db

    def clear_table(self):
        with self.con:
            self.con.execute(f'DELETE FROM {self.get_table_name()}').fetchmany()

    def get_num_rows(self):
        with self.con:
            return self.con.execute(f'SELECT COUNT(*) FROM {self.get_table_name()}').fetchone()[0]

    @abc.abstractmethod
    def create_table(self):
        '''Must override to define table schema
        '''
        with self.con as con:
            con.execute(f"""
                          CREATE TABLE IF NOT EXISTS {self.get_table_name()} (
                              a TEXT UNIQUE,
                              b FLOAT,
                              c FLOAT,
                              d INTEGER 
                          );
                      """)

    def __aenter__(self):
        return self.con

    def _open_connection(self):
        self.con = sl.connect(self.get_db_name())

    @abc.abstractmethod
    def write_many_rows(self, data):
        '''Must override to define row inserts according to table schema
        '''
        sql = f'INSERT INTO {self.get_table_name()} {(None)} values {(None)}'
        with self.con:
            self.con.executemany(sql, data)

    def execute(self, sql):
        '''Runs a single sql query

        :param: sql: str
        '''
        with self.con:
            return self.con.execute(sql).fetchall()

    def __aexit__(self, exc_type, exc, tb):
        with self.con:
            self.clear_table()
            self.con.close()


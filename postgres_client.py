import psycopg2
from psycopg2 import pool

class PostgresSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PostgresSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self, dbname, user, password, host, port):
        if not hasattr(self, '_connection_pool'):
            self._connection_pool = psycopg2.pool.SimpleConnectionPool(
                1,  
                10, 
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print(self._connection_pool)

    def get_connection(self):
        return self._connection_pool.getconn()

    def release_connection(self, connection):
        self._connection_pool.putconn(connection)

    def close_all_connections(self):
        self._connection_pool.closeall()
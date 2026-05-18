import psycopg2
from psycopg2 import pool

db_pool = None

def init_db_pool():
    global db_pool

    db_pool = psycopg2.pool.SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        host="localhost",
        port="5432",
        database="clone_dashboard",
        user="postgres",
        password="postgres"
    )

    print(f"PostgreSQL connection initialised")

def get_connection():

    return db_pool.getconn()

def release_connection(connection):

    db_pool.putconn(connection)
import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="metascandb"
    )
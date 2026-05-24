import os
import pymysql
from dotenv import load_dotenv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR/".env"

def get_connection():
    """Create and return a pymysql connection using credentials from the .env file.

    Reads DB_HOST, DB_USER, DB_PASSWORD, and DB_NAME from the .env file located
    in the same directory as this module.

    Returns:
        pymysql.Connection: An open connection to the configured database.

    Raises:
        ValueError: If any required environment variable is missing.
        pymysql.OperationalError: If the connection to the database fails.
    """
    load_dotenv(ENV_PATH)

    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_name = os.getenv('DB_NAME')

    if db_host == None : raise ValueError('No se pudo encontrar el host')
    if db_user == None : raise ValueError('Usuario no definido')
    if db_password == None : raise ValueError('Password no definido')
    if db_name == None : raise ValueError('Nombre de la base de datos no definido')

    try:
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
    except pymysql.OperationalError:
        raise pymysql.OperationalError('No se pudo conectar con la base de datos')

    return conn
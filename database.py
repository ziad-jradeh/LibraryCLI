import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from configparser import ConfigParser

import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(dir_path, 'database.ini')

DATABASE_NAME = 'librarycli'

connection = None
cur = None

def config(filename=database_path, section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db


def connect(database = DATABASE_NAME):
    """ Connect to the PostgreSQL database server """
    global connection, cur
    try:
        # read connection parameters
        params = config()
        params["database"] = database
        # connect to the PostgreSQL server
        connection = psycopg2.connect(**params)
        connection.autocommit = True
  
        # create a cursor
        cur = connection.cursor()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        
        return [connection, cur]
    
def drop_database():
    [connection, cur] = connect("")
    cur.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME}")
    cur.close()
    connection.close()
    
    
def database_exists(conn, c):
    try:
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        c.execute(f"SELECT datname FROM pg_database;")

        list_database = c.fetchall()
        if (DATABASE_NAME.lower(),) in list_database:
            return True
        return False
    except:
        return False


def create_database():
    
    global connection, cur
    [conn, c] = connect("")
    
    if database_exists(conn, c):
        c.close()
        conn.close()
        print("Database already exists.")
    else:
        c.execute(f"CREATE DATABASE {DATABASE_NAME}")
        c.close()
        conn.close()
        [connection, cur] = connect(DATABASE_NAME)
        cur.execute(open("SQL/create_tables.sql", "r").read())
        prompt = input("An empty database has been created. Would you like to load sample database? [y/n]: ")
        if prompt.lower() == "y":
            cur.execute(open("SQL/insert_sample_db.sql", "r").read())
        connection.commit()
        cur.close()
        connection.close()
        print("Database created successfully.")
    
    return connect(DATABASE_NAME)
    


import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from configparser import ConfigParser

import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
database_path = os.path.join(dir_path, 'server.ini')

DATABASE_NAME = 'librarycli'

global connection, cur
connection, cur = None, None

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
    """ Connect to the PostgreSQL database. If database argument is an empty string,
    then it will connect to the PostgreSQL server without connecting to a databse.
    
    Returns the database connection object and the database cursor object."""
    global connection, cur
    
    try:
        # read connection parameters
        params = config()
        # add database to the connection parameters dictionary
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
    '''A function to drop/delete the database. Returns True if successful, False otherwise.'''
    try:
        # Connect to the PostgreSQL server without connecting to a database
        [connection, cur] = connect("")
        # Drop/delete the database
        cur.execute(f"DROP DATABASE IF EXISTS {DATABASE_NAME} WITH (FORCE)")
        cur.close()
        connection.close()
        return True
    except Exception as e:
        print(e)
        return False
    
def database_exists():
    '''A function that returns True if the database exists and False otherwise.'''
    try:
        # Connect to the PostgreSQL server without connecting to a database
        [conn, c] = connect("")
        # Check if the database exists
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        c.execute(f"SELECT datname FROM pg_database;")

        db_list = c.fetchall()
        c.close()
        conn.close()
        if (DATABASE_NAME.lower(),) in db_list:
            return True
        else:
            return False
    except:
        return False


def create_database():
    '''A function that creates the database if it doesn\'t already exist.'''
    if database_exists():
        return "Database already exists."
    else:
        # Connect to the PostgreSQL Server without a database, to create a new database.
        [connection, cur] = connect("")
        cur.execute(f"CREATE DATABASE {DATABASE_NAME}")
        cur.close()
        connection.close()
        
        #Connect to the new database
        [connection, cur] = connect(DATABASE_NAME)
        # Create the tables
        cur.execute(open("SQL/create_tables.sql", "r").read())
        
        # Ask the user if they want to load a sample database
        prompt = input("An empty database has been created. Would you like to load sample database? [y/n]: ")
        if prompt.lower() == "y":
            cur.execute(open("SQL/insert_sample_db.sql", "r").read())
        connection.commit()
        cur.close()
        connection.close()
        return "Database created successfully."
    
def search_by_name_func(name):
    
                 
        cur.execute(f"""SELECT Cast(book_id As Varchar), b.book_title, CAST(total_pages as Varchar) , g.genre_name, a.author_name,
    CASE 
    WHEN (b.number_copy > ((SELECT COUNT(*) FROM borrowing WHERE book_id=b.book_id) 
                            - (SELECT COUNT(*) FROM returnings WHERE book_id=b.book_id))) 
		  THEN 'True'

    ELSE 'False'

    END AS Availability
    FROM books b
    LEFT JOIN genres AS g ON b.genre_id = g.genre_id
    LEFT JOIN authors AS a ON b.author_id = a.author_id
    WHERE b.book_title ILIKE '%{name}%'
        """)
        return cur.fetchall()
        
  
    
    
  
        
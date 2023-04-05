
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from configparser import ConfigParser
from datetime import date

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
    except Exception as e:
        print(e)
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
def sign_up_func(user_name, password):
    checking_query = f""" select user_name from public.user where user_name = '{user_name}'"""
    cur.execute(checking_query)
    check = cur.fetchone()
    if check is not None:
         pass
    else:
         postgres_insert_query = f""" INSERT INTO public.user (user_name,user_password)  VALUES ('{user_name}','{password}')"""
         cur.execute(postgres_insert_query)
         cur.close()
    return check     
def sign_in_func(user_name, password):
    checking_query = f""" select user_name from public.user where user_name = '{user_name}'and user_password ='{password}'"""
    cur.execute(checking_query)
    check = cur.fetchone()
    return check     
    
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

def search_by_author_func(name):
    
                 
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
    WHERE a.author_name ILIKE '%{name}%'
        """)
        return cur.fetchall()
def most_read_books_func(genre= '%'):
    #how to create as default all genres? 
                 
        cur.execute(f"""SELECT Cast(br.book_id As Varchar), b.book_title, a.author_name, g.genre_name, Cast(COUNT(*) As Varchar) 
FROM borrowing AS br
LEFT JOIN books AS b ON br.book_id = b.book_id
LEFT JOIN genres AS g ON b.genre_id = g.genre_id
LEFT JOIN authors AS a ON b.author_id = a.author_id
WHERE g.genre_name LIKE '%{genre}%'
GROUP BY br.book_id,b.book_title, a.author_name, g.genre_name
ORDER BY COUNT(*) DESC
        """)
        return cur.fetchall()


def get_user_id(user_name):
    cur.execute(f'''
                    SELECT user_id FROM public.user
                    WHERE user_name = '{user_name}'
                ''')
    id = cur.fetchone()
    return id[0]


def get_author_id(author_name):
    cur.execute(f'''
                    SELECT author_id FROM authors
                    WHERE author_name = '{author_name}'
                ''')
    id = cur.fetchone()
    if id is None:
        return None
    else:
        return id[0]

def add_author(author_name):
    cur.execute(f'''
                INSERT INTO authors (author_name)
                VALUES ('{author_name}')
                RETURNING author_id
                ''')
    return cur.fetchone()[0]

def get_genre_id(genre_name):
    
    cur.execute(f'''
                    SELECT genre_id FROM genres
                    WHERE genre_name = '{genre_name}'
                ''')
    id = cur.fetchone()
    if id is None:
        return None
    else:
        return id[0]

def add_genre(genre_name):
    cur.execute(f'''
                INSERT INTO genres (genre_name)
                VALUES ('{genre_name}')
                RETURNING genre_id
                ''')
    return cur.fetchone()[0]

def get_book_id(book_title, author_id):
    cur.execute(f'''
                    SELECT book_id FROM books
                    WHERE book_title = '{book_title}' AND author_id = '{author_id}'
                ''')
    id = cur.fetchone()
    if id is None:
        return None
    else:
        return id[0]

def add_new_book(book_title, author_id, genre_id, pages):
    cur.execute(f'''
                INSERT INTO books (book_title, author_id, genre_id, total_pages, number_copy,available_copy)
                VALUES ('{book_title}', {author_id}, {genre_id}, {pages}, 1,1)
                RETURNING book_id
                ''')
    return cur.fetchone()[0]

def increase_book_copies(book_id):
    cur.execute(f'''
                UPDATE books
                SET number_copy = number_copy + 1,available_copy = available_copy +1
                WHERE book_id = {book_id}
                RETURNING book_id
                ''')
    return cur.fetchone()

def book_added_record(books_id, users_id):
    
    cur.execute(f'''
                INSERT INTO added_book (book_id, user_id, added_date)
                VALUES ({books_id}, {users_id}, '{date.today()}')
                ''')

def most_read_genres_func():
    cur.execute(f'''SELECT  g.genre_name, Cast(COUNT(*) As Varchar) 
                FROM read_book AS r
                LEFT JOIN books AS b ON r.book_id = b.book_id
                LEFT JOIN genres AS g ON b.genre_id = g.genre_id
                GROUP BY g.genre_name
                ORDER BY COUNT(*) DESC LIMIT 5
                ''')
    return cur.fetchall()

def most_read_authors_func():
    cur.execute(f'''SELECT  a.author_name, Cast(COUNT(*) As Varchar) 
                FROM read_book AS r
                LEFT JOIN books AS b ON r.book_id = b.book_id
                LEFT JOIN authors AS a ON b.author_id = a.author_id
                GROUP BY a.author_name
                ORDER BY COUNT(*) DESC LIMIT 3
                ''')
    return cur.fetchall()
def recently_added_func(genre='%'):
    #how to create as default all genres? 
         
    cur.execute(f"""SELECT Cast(br.book_id As Varchar), b.book_title, a.author_name,Cast(b.total_pages As Varchar) , g.genre_name,u.user_name,
            CASE 
            WHEN (b.number_copy > ((SELECT COUNT(*) FROM borrowing WHERE book_id=br.book_id) 
                                    - (SELECT COUNT(*) FROM returnings WHERE book_id=br.book_id))) 
                THEN 'True'

            ELSE 'False'

            END AS Availability
            FROM added_book AS br
            LEFT JOIN books AS b ON br.book_id = b.book_id
            LEFT JOIN authors AS a ON b.author_id = a.author_id
            LEFT JOIN genres AS g ON b.genre_id = g.genre_id
            LEFT JOIN public.user AS u ON br.user_id = u.user_id
            WHERE g.genre_name LIKE '%{genre}%'
            GROUP BY br.book_id,b.book_title, a.author_name,b.total_pages, g.genre_name,u.user_name,b.number_copy,br.added_date
            order by br.added_date desc
        """)
    
    return cur.fetchmany(5)
def check_if_borrowed_before(user_id,book_id):
    cur.execute(f""" SELECT borrow_id from borrowing
          where (SELECT COUNT(*) FROM borrowing WHERE book_id = {book_id} and user_id ={user_id}) 
                                    > (SELECT COUNT(*) FROM returnings WHERE book_id = {book_id} and user_id ={user_id})
            
               
    """)
    check =cur.fetchone()
    if check is None:
        return None
    else:
     return check[0]
def borrow_book_func(book_id):
    cur.execute(f""" SELECT available_copy from books  
               WHERE book_id = {book_id}
    
    """)
    number_copy =cur.fetchone()
    if number_copy is None:
        return None
    else:
     return number_copy[0]
def add_into_borrow_func(user_id,book_id):
     cur.execute(f""" insert into borrowing( borrow_date,user_id,book_id) 
                      values('{date.today()}',{user_id},{book_id})
    
    """)
def decrease_available_copy(book_id):
    cur.execute(f'''
                UPDATE books
                SET available_copy = available_copy - 1
                WHERE book_id = {book_id}
                RETURNING book_id
                ''')
def increase_available_copy(book_id):
    cur.execute(f'''
                UPDATE books
                SET available_copy = available_copy + 1
                WHERE book_id = {book_id}
                RETURNING book_id
                ''')

def add_into_return_func(user_id,book_id):
       cur.execute(f""" insert into returnings( return_date,user_id,book_id) 
                      values('{date.today()}',{user_id},{book_id})
    
    """)
       
def book_exists(book_id):
    cur.execute(f'''
                SELECT book_id FROM books WHERE book_id = {book_id}
                ''')
    id = cur.fetchone()
    if id is None:
        return False
    else:
        return True
    
def mark_book_as_read(book_id, user_id):
    cur.execute(f'''
                SELECT book_id FROM read_book WHERE book_id = {book_id} AND user_id = {user_id}
                ''')
    already_read = cur.fetchone()
    if already_read is None:
        cur.execute(f'''
                INSERT INTO read_book (book_id, user_id) VALUES ({book_id}, {user_id})
                ''')

def mark_book_as_fav(book_id, user_id):
    cur.execute(f'''
                SELECT book_id FROM favorite WHERE book_id = {book_id} AND user_id = {user_id}
                ''')
    already_read = cur.fetchone()
    if already_read is None:
        cur.execute(f'''
                INSERT INTO favorite (book_id, user_id) VALUES ({book_id}, {user_id})
                ''')
        
def user_read_books(user_id):
    cur.execute(f'''
                SELECT Cast(book_id As Varchar), book_title, CAST(total_pages as Varchar) , genre_name, author_name,
                                CASE 
                                WHEN available_copy > 0 THEN 'True'
                                ELSE 'False'
                                END AS Availability
                FROM books
                INNER JOIN read_book USING (book_id)
                INNER JOIN genres USING (genre_id)
                INNER JOIN authors USING (author_id)
                WHERE user_id = {user_id}
                ORDER BY book_id
                ''')
    return cur.fetchall()


def user_fav_books(user_id):
    cur.execute(f'''
                SELECT Cast(book_id As Varchar), book_title, CAST(total_pages as Varchar) , genre_name, author_name,
                                CASE 
                                WHEN available_copy > 0 THEN 'True'
                                ELSE 'False'
                                END AS Availability
                FROM books
                INNER JOIN favorite USING (book_id)
                INNER JOIN genres USING (genre_id)
                INNER JOIN authors USING (author_id)
                WHERE user_id = {user_id}
                ORDER BY book_id
                ''')
    return cur.fetchall()
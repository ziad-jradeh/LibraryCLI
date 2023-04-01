from tkinter import E
import typer
from rich.console import Console
from rich.table import Table
from typing import Optional

from  database import *


console = Console()
app = typer.Typer()


@app.command()
def start(none: Optional[str] = typer.Argument(None)):
    '''Check if the database is available, and if not create a new database.'''
    
    typer.secho(create_database())
    typer.secho(f'''Welcome to Library CLI!\nUse command '--help' to see the possible commands''', fg=typer.colors.GREEN)

def sign_in():
    [connection, cur] = connect()
    check = None
    print(" Please sign in first  ")
    username = input('Enter  user name ')
    password = input(' Enter password ')
    while not check:
        try:
            
             check = sign_in_func(username,password)
             if check is None:
                raise ValueError
        except ValueError:
                print("\033[1;31m user name or password error!  ")
                username = input('\033[1;31m Enter again user name ')
                password = input('\033[1;31m Enter again password ')
        except (Exception, psycopg2.DatabaseError):
             print("\033[1;31m Error data base connection")
             break
        else:
           
            typer.echo(f" Congrats! you are signed in!")

            break 
    if connection is not None:
        connection.close()
    return username     
@app.command("sign_up")
def sign_up(username: str, password:str):
    # TODO: Add user with name {username} and {password} to database table
    [connection, cur] = connect()
    check = not None
    while check:
        try:
             check = sign_up_func(username,password)
             if check is not None:
                raise ValueError
        except ValueError:
                print("\033[1;31m The user name is occupied ")
                username = input('\033[1;31m Enter another user name ')
                password = input('\033[1;31m Enter password ')

                
        except (Exception, psycopg2.DatabaseError):
             print("\033[1;31m Error data base connection")
             break
        else:
           
            typer.echo("\033[1;32m Congrats! you are registered!")
            break      
        
    if connection is not None:
        connection.close()
        print('Database connection closed.')

### For testing purposes, can be removed later
@app.command("del_database")
def del_database(none: Optional[str] = typer.Argument(None)):
    '''Delete the current database. User start after to create a new one.'''
    
    if drop_database():
        typer.secho("Database Deleted!")
        typer.secho("You can now use the command \"start\" to make a new database.")


@app.command("search_by_name")
def search_by_name(name:str):
   
    [connection, cur] = connect()
    try:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("book_id", style="dim", width=10)
        table.add_column("book_title", style="dim", min_width=10, justify=True)
        table.add_column("total_pages", style="dim", width=5)
        table.add_column("genre_name", style="dim", min_width=10, justify=True)
        table.add_column("author_name", style="dim", min_width=10, justify=True)
        table.add_column("Availability", style="dim", width=15)
        
        print(f"I am looking for {name}... That what we have for you:")
        rows = search_by_name_func(name)

        for row in rows:
            table.add_row(*list(row))
        console.print(table)

    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()
            print('Database connection closed.')

@app.command("search_by_author")
def search_by_author(name:str):
   
    [connection, cur] = connect()
    try:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("book_id", style="dim", width=10)
        table.add_column("book_title", style="dim", min_width=10, justify=True)
        table.add_column("total_pages", style="dim", width=10)
        table.add_column("genre_name", style="dim", min_width=10, justify=True)
        table.add_column("author_name", style="dim", min_width=10, justify=True)
        table.add_column("Availability", style="dim", width=15)
        
        print(f"I am looking for {name}... That what we have for you:")
        rows = search_by_author_func(name)

        for row in rows:
            table.add_row(*list(row))
        console.print(table)

    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()
            print('Database connection closed.')


@app.command("add_book")
def add_book():
    
    # Check if database already exists
    if not database_exists():
        print("Database is not created yet, run the command \"start\" to make a new database.")
        return
    
    ### TODO: Check if user is logged in
    user_name = sign_in()
    # Start a connection to the database
    [connection, cur] = connect()
    
    # A loop for user inputs
    while True:
        try:
            book_title = input("Name of the book: ")
            if book_title == '':
                typer.secho("Please enter a book title. Cannot be empty!", fg=typer.colors.RED)
                continue
            author_name = input("Author: ")
            if author_name == '':
                typer.secho("Please enter an author name. Cannot be empty!", fg=typer.colors.RED)
                continue
            pages = int(input("# Pages: "))
            if pages <= 0:
                typer.secho("Invalid input. Try again", fg=typer.colors.RED)
                continue
            genre_name = input("Genre: ")
            if genre_name == '':
                typer.secho("Please enter genre name. Cannot be empty!", fg=typer.colors.RED)
                continue
            break
        except:
            typer.secho("Invalid input. Try again", fg=typer.colors.RED)
            continue
            
    # Try to find the author, if not found add a new author
    author_id = get_author_id(author_name)
    if author_id is None:
        author_id = add_author(author_name)
    
    
    genre_id = get_genre_id(genre_name)
    if genre_id is None:
        genre_id = add_genre(genre_name)
    
    
    book_id = get_book_id(book_title, author_id)
    if book_id is None:
        book_id = add_new_book(book_title, author_id, genre_id, pages)
        typer.secho(f'''A new book has been added!''', fg=typer.colors.GREEN)
        user_id = get_user_id(user_name)
        book_added_record(book_id,user_id)
    else: 
        book_id = increase_book_copies(book_id)
        typer.secho(f'''The book already exists! The number of copies has been increased by one!''', fg=typer.colors.GREEN)
    
    
    ### TODO: Add the book added record
    # user_id = 1
    # book_added_record(book_id, user_id)
    
    cur.close()
    connection.close()

@app.command("most_read_books")
def most_read_books(genre:str):
   
    [connection, cur] = connect()
    try:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("book_id", style="dim", width=10)
        table.add_column("book_title", style="dim", min_width=10, justify=True)
        table.add_column("author_name", style="dim", min_width=10, justify=True)
        table.add_column("genre_name", style="dim", min_width=10, justify=True)
        table.add_column("count", style="dim", width=15)
        
        print(f"I am looking for {genre}... That what we have for you:")
        #this string just for test
        rows = most_read_books_func(genre)

        for row in rows:
            table.add_row(*list(row))
        console.print(table)

    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()
            print('Database connection closed.')


@app.command("recently_added")
def recently_added(genre:Optional[str] = typer.Argument(None)):
   
    [connection, cur] = connect()
    try:
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("book_id", style="dim", width=10)
        table.add_column("book_title", style="dim", min_width=10, justify=True)
        table.add_column("author_name", style="dim", min_width=10, justify=True)
        table.add_column("# Pages", style="dim", min_width=10, justify=True)
        table.add_column("genre_name", style="dim", min_width=10, justify=True)
        table.add_column("added_by", style="dim", min_width=10, justify=True)
        table.add_column("vailabilty", style="dim", min_width=10, justify=True)
        print(f"I am looking for {genre}... That what we have for you:")
        #this string just for test
        rows = recently_added_func(genre)

        for row in rows:
            table.add_row(*list(row))
        console.print(table)

    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()
            print('Database connection closed.')

    
    
if __name__ == "__main__":
    app()

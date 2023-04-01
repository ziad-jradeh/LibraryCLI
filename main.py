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
@app.command("sign_up")
def sign_up(username: str, password:str):
    # TODO: Add user with name {username} and {password} to database table
    [connection, cur] = connect()
    check = not None
    while check:
        try:

<<<<<<< Updated upstream
@app.command("sign_up")
def sign_up(username: str, password:str):
    # TODO: Add user with name {username} and {password} to database table
    [connection, cur] = connect()
    check = not None
    while check:
        try:
                
=======
>>>>>>> Stashed changes
                check = sign_up_func(username,password)
                if check is not None:
                      raise ValueError
        except ValueError:
                print("\033[1;31m The user name is occupied ")
                username = input('\033[1;31m Enter another user name ')
                password = input('\033[1;31m Enter password ')
<<<<<<< Updated upstream
                
        except (Exception, psycopg2.DatabaseError):
             print("\033[1;31m Error data base connection")
             break
        else:
           
            typer.echo("\033[1;32m Congrats! you are registered!")
            break      
        
    if connection is not None:
        connection.close()
        print('Database connection closed.')
=======
>>>>>>> Stashed changes

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

    
    
    
if __name__ == "__main__":
    app()

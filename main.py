
import typer
from rich.console import Console
from rich.table import Table
from typing import Optional

from  database import *


console = Console()
app = typer.Typer()

def print_table(columns = [], title = '', rows = []):
    table = Table(*columns, title=title, show_header=True, header_style="bold blue", min_width=100, title_style="bold white on blue")
    for i, row in enumerate(rows):
            table.add_row(str(i+1), *list(row))
    console.print(table)


@app.command()
def start(none: Optional[str] = typer.Argument(None)):
    '''Check if the database is available, and if not create a new database.'''
    
    typer.secho(create_database())
    typer.secho(f'''Welcome to Library CLI!\nUse command '--help' to see the possible commands''', fg=typer.colors.GREEN)


def sign_in():
    [connection, cur] = connect()
    check = None
    print("Please sign in first...")
    username = input('Enter  user name: ')
    password = input('Enter password: ')
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
        cur.close()
        connection.close()
    return username


@app.command("sign_up")
def sign_up(username: str, password:str):
    '''Registers a new user with username and password. if the username is occupied, it notifys and provide the user for another input.  '''
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
        cur.close()
        connection.close()


### For testing purposes, can be removed later
@app.command("del_database")
def del_database(none: Optional[str] = typer.Argument(None)):
    '''Delete the current database. User start after to create a new one.'''
    
    if drop_database():
        typer.secho("Database Deleted!")
        typer.secho("You can now use the command \"start\" to create a new database.")


@app.command("search_by_name")
def search_by_name(name:str):
    '''search a book by its title and displays it with its detail information. '''
    [connection, cur] = connect()
    try:
        rows = search_by_name_func(name)
        print_table(["#", 'Book ID', 'Title', 'Author', '# Pages', 'Genre', 'Availability'], f'Search results for: {name}', rows)
    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()


@app.command("search_by_author")
def search_by_author(name:str):
    '''search a book by the author name and displays it with its detail information. '''
    [connection, cur] = connect()
    try:
        rows = search_by_author_func(name)
        print_table(["#", 'Book ID', 'Title', 'Author', '# Pages', 'Genre', 'Availability'], f'Search results for: {name}', rows)
    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()


@app.command("recently_added")
def recently_added(genre:Optional[str] = typer.Argument('%')):
    '''displays all the books in the library with the most recent on the top.'''
    [connection, cur] = connect()
    try:
        #this string just for test
        rows = recently_added_func(genre)
        print_table(["#", 'Book ID', 'Title', 'Author', '# Pages', 'Genre', 'Availability'], f'Recently added books:', rows)
    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()


@app.command("most_read_books")
def most_read_books(genre:Optional[str] = typer.Argument('%')):
    ''' it displays the most read books by users of the library.'''
    [connection, cur] = connect()
    try:
        #this string just for test
        rows = most_read_books_func(genre)
        print_table(["#", 'Book ID', 'Title', 'Author', 'Genre', 'Count'], f'Most read books:', rows)
    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
           cur.close()
           connection.close()

@app.command("most_favorite_books")
def most_favorite_books(genre:Optional[str] = typer.Argument('%')):
    '''it displays the most favored books by the users of the library.'''
    [connection, cur] = connect()
    try:
        rows = most_favorite_books_func(genre)
        print_table(["#", 'Book ID', 'Title', 'Author', 'Genre', 'Count'], f'Most favorite books:', rows)

    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
           cur.close()
           connection.close()
        print('Database connection closed.')

@app.command("most_read_genres")
def most_read_genres():
    '''it displays the most read genres and their number.'''
    [connection, cur] = connect()
    try:
        rows = most_read_genres_func()
        print_table(["#", 'Genre', 'Count'], f'Most read genres:', rows)
    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()


@app.command("most_read_authors")
def most_read_authors():
    '''it displays the most read authors and their number.'''
    [connection, cur] = connect()
    try:
        rows = most_read_authors_func()
        print_table(["#", 'Author', 'Count'], f'Most read authors:', rows)
    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()


@app.command("add_book")
def add_book():
    ''' it provides the user to add any book to the library.But the user has to signed in first.'''
    # Check if database already exists
    if not database_exists():
        print("Database is not created yet, run the command \"start\" to make a new database.")
        return
    
    ### TODO: Check if user is logged in
    user_name = sign_in()
    # Start a connection to the database
    [connection, cur] = connect()
    
    try:
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
    except Exception as error:
        print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()


@app.command("borrow_book")
def borrow_book(book_id:int):
    ''' it provides the user to borrow any book from the library.But the user has to signed in first.'''
     # Check if database already exists
    if not database_exists():
        print("Database is not created yet, run the command \"start\" to make a new database.")
        return
    
    user_name = sign_in()
    
    # Start a connection to the database
    [connection, cur] = connect()
    user_id = get_user_id(user_name)
    
         #check if the user already borrowed the book or not
    availabilty = borrow_book_func(book_id )
    if availabilty == 0 or availabilty is None:
           typer.secho(f"Sorry book {book_id} is not available Try again", fg=typer.colors.RED)
    else:
        check = check_if_borrowed_before(user_id,book_id)
        if check is None:  
           add_into_borrow_func(user_id,book_id)
           decrease_available_copy(book_id)
           typer.secho(f"You borrowed book {book_id} ", fg=typer.colors.GREEN)
        else:
             typer.secho(f"Sorry you have already borrowed book {book_id}. Try another", fg=typer.colors.RED)
    if connection is not None:
            cur.close()
            connection.close()


@app.command("return_book")
def return_book(book_id:int):
    ''' it provides the user to return the book he/she borrowed.But the user has to signed in first.'''
     # Check if database already exists
    if not database_exists():
        print("Database is not created yet, run the command \"start\" to make a new database.")
        return
    
    user_name = sign_in()
    
    # Start a connection to the database
    [connection, cur] = connect()
    user_id = get_user_id(user_name)
    check = check_if_borrowed_before(user_id,book_id)
    if check is None:
        typer.secho(f"Sorry you didn't borrow book {book_id} Try another ", fg=typer.colors.RED)
    else:
        add_into_return_func(user_id,book_id)
        increase_available_copy(book_id)
        typer.secho(f"You returned book {book_id} ", fg=typer.colors.GREEN)
    if connection is not None:
            cur.close()
            connection.close()
            

@app.command("mark_read")
def mark_read(book_id: str):
    ''' it enables the user to mark any book as read.But the user has to signed in first.'''
    # Check if database already exists
    if not database_exists():
        print("Database is not created yet, run the command \"start\" to make a new database.")
        return
    
    user_name = sign_in()
    
    [connection, cur] = connect()
    
    if book_exists(book_id):
        user_id = get_user_id(user_name)
        mark_book_as_read(book_id, user_id)
        typer.secho(f'Book {book_id} has been marked as read.')
    else:
        typer.secho(f'Book {book_id} does not exist. Make sure you are providing the correct book_id.')
        
    cur.close()
    connection.close()


@app.command("fav_book")
def fav_book(book_id: str):
    ''' it enables the user to mark any book as favorite.But the user has to signed in first.'''
    # Check if database already exists
    if not database_exists():
        print("Database is not created yet, run the command \"start\" to make a new database.")
        return
    
    user_name = sign_in()
    
    [connection, cur] = connect()
    
    if book_exists(book_id):
        user_id = get_user_id(user_name)
        mark_book_as_fav(book_id, user_id)
        typer.secho(f'Book {book_id} has been marked as favorite.')
    else:
        typer.secho(f'Book {book_id} does not exist. Make sure you are providing the correct book_id.')
    
    cur.close()
    connection.close()
    
    
@app.command("my_books")
def my_books():
    ''' it displays all the books of a user in a two table, read and favorite.But the user has to signed in first.'''
    # Check if database already exists
    if not database_exists():
        print("Database is not created yet, run the command \"start\" to make a new database.")
        return
    
    user_name = sign_in()
    
    try:
        [connection, cur] = connect()
        user_id = get_user_id(user_name)
    
        read_results = user_read_books(user_id)
        print_table(["#", 'Book ID', 'Title', 'Author', '# Pages', 'Genre', 'Availability'], f'Your read books are:', read_results)
        
        fav_results = user_fav_books(user_id)
        print_table(["#", 'Book ID', 'Title', 'Author', '# Pages', 'Genre', 'Availability'], f'Your favorite books are:', fav_results)
        
    except Exception as error:
        print(error)      
    finally: 
        if connection is not None:
            cur.close()
            connection.close()


@app.command("statistics")
def statistics():
    ''' it displays summary of all the books the user read in terms of number of books, authors,genres and pages.But the user has to signed in first.'''
    ### Check if user is logged in
    user_name = sign_in()
    # Start a connection to the database
    [connection, cur] = connect()
    try:
        table = Table(show_header=True, header_style="bold blue", title = f'{user_name}\'s statistics:', title_style="bold white on blue")
        
        table.add_column("Statistic", width=30)
        table.add_column("Number", width=10)
        
        Value1 = my_read_books(user_name)
        Value2 = my_read_authors(user_name)
        Value3 = my_read_genres(user_name)
        Value4 = my_read_pages(user_name)

        table.add_row("Books you read", str(Value1))
        table.add_row("Authors you read", str(Value2))
        table.add_row("Genres you read", str(Value3))
        table.add_row("Total pages you read", str(Value4))

        console.print(table)

    except (Exception, psycopg2.DatabaseError) as error:
         print(error)      
    finally: 
        if connection is not None:
           cur.close()
           connection.close()
        

if __name__ == "__main__":
    app()

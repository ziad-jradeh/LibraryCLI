import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
import psycopg2

console = Console()

app = typer.Typer()
conn = psycopg2.connect(
    host="localhost",
	database="Library",
	user="postgres",
	password="Fenyx")

@app.command("start")
def start():
    typer.secho(f'''Welcome to Library CLI!\n\n
        You can execute command '--help' to see the possible commands''', fg=typer.colors.GREEN)
    # TODO: connect to database

# This is how you can get arguments, here username is a mandatory argument for this command.
@app.command("sign_up")
def sign_up(username: str, password:str):
    # TODO: Add user with name {username} and {password} to database table
    check = not None
    while check:
        try:
                cur = conn.cursor()
                checking_query = f""" select user_name from public.user where user_name = '{username}'"""
                cur.execute(checking_query)
                check = cur.fetchone()
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
            postgres_insert_query = f""" INSERT INTO public.user (user_name,user_password)  VALUES ('{username}','{password}')"""
            cur.execute(postgres_insert_query)
            cur.close()
            conn.commit()
            typer.echo("\033[1;32m Congrats! you are registered!")
            break      
        
    if conn is not None:
        conn.close()
        
@app.command("sign_in")
def sign_in(username: str, password:str):
    check = None
    while not check:
        try:
                cur = conn.cursor()
                checking_query = f""" select user_name from public.user where user_name = '{username}' and user_password='{password}'"""
                cur.execute(checking_query)
                check = cur.fetchone()
                if check is None:
                      raise ValueError
        except ValueError:
                print("\033[1;31m Error user name and password ")
                username = input('\033[1;31m Enter again user name  =')
                password = input('\033[1;31m Enter again password  =')
                
        except (Exception, psycopg2.DatabaseError):
             print("\033[1;31m Error data base connection")
             
        else:
            typer.echo("\033[1;32m you are signed in!")
            break      
        
    if conn is not None:
        conn.close()
@app.command("add_book")
def add_book():
    typer.echo(f"Please provide book details!")
    try:   
         cur = conn.cursor()
         title = input ("Title: ")
         author = (input ("Author: "))
         pages = input ("No. of pages: ")
         genre = (input ("Genre: "))
         quantity= int(input ("Quantity: "))
         select_query = f"""select number_copy from books where book_title = '{title}'and author = '{author}' """
         cur.execute(select_query)
         copy_1 = cur.fetchone()      
    except(Exception, psycopg2.DatabaseError):
            print("Error")
    else:
        if copy_1 is not None:
            updated_quantity = copy_1[0] + quantity
            update_query = f"""update books set number_copy = '{updated_quantity}'  where book_title = '{title}' and author = '{author}' """
            cur.execute(update_query)
            typer.echo(f"\033[1;32m Number of book copy successfully updated!")	
        else:
            insert_query = f""" INSERT INTO books (book_title,author,genre,Total_pages,number_copy) VALUES ('{title}','{author}','{genre}','{pages}','{quantity}')"""
            cur.execute(insert_query)
            typer.echo(f"\033[1;32m The book is successfully added!")

        cur.close()
        conn.commit()
# Example function for tables, you can add more columns/row.
@app.command("display_table")
def display_table():
    table = Table(show_header=True, header_style="bold blue")
    table.add_column("Column 1", style="dim", width=10)
    table.add_column("Column 2", style="dim", min_width=10, justify=True)
    
    table.add_row('Value 1', 'Value 2')
    table.add_row('Value 3', 'Value 4')
    table.add_row('Value 5', 'Value 6')

    console.print(table)

if __name__ == "__main__":
    app()
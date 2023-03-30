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


### For testing purposes, can be removed later
@app.command("del_database")
def del_database(none: Optional[str] = typer.Argument(None)):
    '''Delete the current database. User start after to create a new one.'''
    
    if drop_database():
        typer.secho("Database Deleted!")
        typer.secho("You can now use the command \"start\" to make a new database.")

    
if __name__ == "__main__":
    app()

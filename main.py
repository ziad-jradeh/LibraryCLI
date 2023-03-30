import typer
from rich.console import Console
from rich.table import Table
from typing import Optional

from  database import *


console = Console()

app = typer.Typer()


@app.command()
def start(none: Optional[str] = typer.Argument(None)):
    create_database()
    typer.secho(f'''Welcome to Library CLI!\nUse command '--help' to see the possible commands''', fg=typer.colors.GREEN)


@app.command("del_database")
def del_database(none: Optional[str] = typer.Argument(None)):
    drop_database()
    typer.secho("Database deleted.")

if __name__ == "__main__":
    app()
import typer
from rich.console import Console
from rich.table import Table
from typing import Optional
import psycopg2

console = Console()

app = typer.Typer()

@app.command("search_by_name")
def search_by_name(name:str):
    print(f"I am looking for {name}... That what we have for you:")
    SELECT b.book_id, b.book_title, b.total_pages, g.genre_name, a.author_name 
    FROM books b
    LEFT JOIN genres AS g ON b.genre_id = g.genre_id
    LEFT JOIN author AS a ON b.author_id = a.author_id
    WHERE b.book_title LIKE '%name%'
    CASE 
    WHERE (b.number_copy > ((SELECT COUNT(*) FROM borrowing WHERE book_id=b.book_id) 
                            - (SELECT COUNT(*) FROM return WHERE book_id=b.book_id)) THEN 'True'

    ELSE 'False'

    END AS 'Availability';


# table = Table(show_header=True, header_style="bold blue")
#     table.add_column("Column 1", style="dim", width=10)
#     table.add_column("Column 2", style="dim", min_width=10, justify=True)
    
#     table.add_row('Value 1', 'Value 2')
#     table.add_row('Value 3', 'Value 4')
#     table.add_row('Value 5', 'Value 6')

#     console.print(table)

# if __name__ == "__main__":
#     app()
    
    
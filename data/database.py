import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path
        self._setup_tables()

    def connect(self):
        con = sqlite3.connect(self.path)
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA foreign_keys = ON")
        return con

    def _setup_tables(self):
        """Maak basis tabellen aan"""
        with self.connect() as con:
            cur = con.cursor()

            # Users tabel (voorbeeld)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            """)

    def add_column(self, table_name: str, column_name: str, column_type: str):
        """Voeg kolom toe aan bestaande tabel als deze nog niet bestaat"""
        with self.connect() as con:
            cur = con.execute(f"PRAGMA table_info({table_name})")
            columns = [row["name"] for row in cur.fetchall()]
            if column_name not in columns:
                con.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

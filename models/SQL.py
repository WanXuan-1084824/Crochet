import sqlite3
from data.database import Database

class Queries:
    def __init__(self, db: Database):
        self.db = db

    def create_user(self, email: str, password: str):
        """Voeg een nieuwe gebruiker toe"""
        with self.db.connect() as con:
            con.execute(
                "INSERT INTO users (email, password) VALUES (?, ?)",
                (email, password)
            )

    def get_user_by_email(self, email: str):
        """Check of gebruiker al bestaat"""
        with self.db.connect() as con:
            cur = con.execute("SELECT * FROM users WHERE email = ?", (email,))
            return cur.fetchone()

    def login_user(self, email: str, password: str):
        """Controleer of een gebruiker bestaat met email + wachtwoord."""
        with self.db.connect() as con:
            cur = con.execute(
                "SELECT * FROM users WHERE email = ? AND password = ?",
                (email, password)
            )
            return cur.fetchone()

    def email_check(self, email: str):
        """Controleer of een e-mailadres bestaat in de database."""
        with self.db.connect() as con:
            cur = con.execute(
                "SELECT 1 FROM users WHERE email = ?",
                (email,)
            )
            return cur.fetchone() is not None

    def get_project(self, project_id):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT *
                FROM crochet_projects
                WHERE id = ?
            """, (project_id,))

            return cur.fetchone()

    def get_projects(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM crochet_projects")
            return cur.fetchall()

    def get_terms(self):
        with self.db.connect() as con:
            cur = con.cursor()

            cur.execute("SELECT * FROM haaktermen")

            return cur.fetchall()

    def get_term(self, term_id):
        with self.db.connect() as con:
            cur = con.cursor()
            con.row_factory = sqlite3.Row
            cur.execute(
                "SELECT * FROM haaktermen WHERE id = ?",
                (term_id,)
            )

            return cur.fetchone()

    # In queries.py
    def get_haaktermen(self):
        with self.db.connect() as con:
            cur = con.cursor()
            cur.execute("SELECT id, naam, afkorting, url FROM haaktermen")
            return cur.fetchall()  # lijst van tuples (id, naam, afkorting, url)
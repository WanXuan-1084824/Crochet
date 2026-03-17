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
        with self.db.connect() as con:
            cur = con.execute("SELECT * FROM users WHERE email = ?", (email,))
            return cur.fetchone()  # geeft None als niet gevonden

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

    def get_mochi_cat_info(self):
        with self.db.connect() as con:
            cur = con.execute('SELECT * FROM crochet_projects WHERE title = ?', ("Mochi Cat",))
            return cur.fetchone()
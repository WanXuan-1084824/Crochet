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

            # Users tabel
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            """)

            cur.execute("SELECT id FROM users WHERE id = 1")
            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO users (email, password)
                    VALUES (?, ?)
                """, ("hualing@email.com", "secret"))

            # Crochet_Projects tabel
            cur.execute("""
                        CREATE TABLE IF NOT EXISTS crochet_projects (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        photo TEXT,
                        pattern TEXT,
                        user_id TEXT,
                        created_at DATE DEFAULT CURRENT_DATE,
                        supplies TEXT,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                        )
                    """)

            cur.execute("SELECT 1 FROM crochet_projects WHERE title = ?", ("Mochi Cat",))

            if not cur.fetchone():
                pattern = """
Cat with one color pattern:
R1: 6 sc in MR [6]
R2: inc * 6 [12]
R3: (sc, inc) * 6 [18]
R4: (sc, inc, sc) * 6 [24]
R5: (3sc, inc) * 6 [30]
R6-9: sc around [30]
R10: (3sc, dec) * 6 [24]
Tail: ch7, from the second chain from the hook: hdc, 5slst
R11: dec, 2sc, bo, dec, sc, dec, bo, sc, dec, sc, bo, dec, sc, dec, bo 2sc [18]
Add stuffing
R12: (sc, dec) * 6 [12]
R13: dec * 6 [6]
Leave a medium tail, fasten off and sew the hole closed
                     
Cat ears 
Right ears:  
Ch3, from the 2nd chain from the hook: hdc, dc, slst to R3 
Sew to secure and hide the ends 
                     
Left ear: ch3, from the  2nd chain from the hook: hdc, dc, slst to R5 
Sew to secure and hide the ends 
                     
Face details 
Use black thread to embroider the eyes on R7, 5 stiches apart 
Embroider the nose on R8, centered between the eyes 
Embroider the wiskers 1 stitch apart from the eyes, on R7 use and R8 add blush 
Use brown yarn to make stripes on the cat 
                     
Cat with two colors pattern: 
Repeat R1 to R5 as one color cat 
R5: (3sc, inc) * 3, (change color 2sc), sc, inc, (3sc, inc) *2 [30] 
R6: 14 sc, (change color 4sc), 12 sc [30] 
R7: 13sc, (change color 6sc), 11sc [30] 
R8-20: follow the same pattern as R6 to R13 in the one color cat pattern, but with the another color yarn 
                     
Then embroider the face details"""

                supplies = """
            2mm chenille yarn
            Black thread
            Stitch marker
            Needle
            5 mm eyes
            2.5 mm hook
            Tweezers
            Scissors
            Glue
            Stuffing
            Black felt
            Blush"""

                cur.execute("""
                                         INSERT INTO crochet_projects
                                         (title, photo, pattern, user_id, created_at, supplies)
                                         VALUES (?, ?, ?, ?, CURRENT_DATE, ?)
                                     """, (
                    "Mochi Cat",
                    "https://www.youtube.com/embed/Iht1z8kpQRA",
                    pattern,
                    1,
                    supplies
                ))

            con.commit()

    def add_column(self, table_name: str, column_name: str, column_type: str):
        """Voeg kolom toe aan bestaande tabel als deze nog niet bestaat"""
        with self.connect() as con:
            cur = con.execute(f"PRAGMA table_info({table_name})")
            columns = [row["name"] for row in cur.fetchall()]
            if column_name not in columns:
                con.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
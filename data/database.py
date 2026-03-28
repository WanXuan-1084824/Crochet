import sqlite3
haaktermen = [
                ("magic ring", "mr", "https://www.youtube.com/embed/hNq4d1w-eQA"),
                ("single crochet", "sc", "https://www.youtube.com/embed/3DNRFfbFZ3o"),
                ("increase", "inc", "https://www.youtube.com/embed/5aDHW7yOICk"),
                ("decrease", "dec", "https://www.youtube.com/embed/fB64nsKHGuQ"),
                ("chain", "ch", "https://www.youtube.com/embed/hqyEXkgjTL8"),
                ("half double crochet", "hdc", "https://www.youtube.com/embed/BRZfDGtN2vE"),
                ("slip stitch", "sl st", "https://www.youtube.com/embed/axhed3wSm3U"),
                ("bobble stitch", "bo", "https://www.youtube.com/embed/bb2nmzSEP-Q"),
                ("double crochet", "dc", "https://www.youtube.com/embed/vmk85y1du_4"),
                ("back loops only", "blo", "https://www.youtube.com/embed/RSNkSH6rMYE"),
                ("treble crochet", "tr", "https://www.youtube.com/embed/_9ba2Vldelo"),
                ("picot stitch", "picot", "https://www.youtube.com/embed/8bVWzFZqqfk"),
                ("front loops only", "flo", "https://www.youtube.com/embed/1FEHqMXULNw"),
            ]
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
        """Maak alle tabellen en basisdata"""
        with self.connect() as con:
            cur = con.cursor()

            # -------------------------
            # Gebruikers tabel
            # -------------------------
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
                cur.execute("""INSERT INTO users (email, password) VALUES (?, ?) """, ("bingjing@email.com", "secret"))


            # -------------------------
            # Community - vragen tabel
            # -------------------------
            cur.execute("""
            CREATE TABLE IF NOT EXISTS vragen (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                inhoud TEXT NOT NULL,
                media TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """)

            cur.execute("SELECT COUNT(*) FROM vragen")
            count = cur.fetchone()[0]

            if count == 0:
                cur.execute("INSERT INTO vragen (user_id, title, inhoud, media) VALUES (1, 'Welke haaknaald voor gebruik?', 'Ik heb een wol gekocht bij de Zeeman, hoe kan ik weten welke haaknaald ik moet gebruiken voor die wol?', 'wol.jpeg')")
                cur.execute("INSERT INTO vragen (user_id, title, inhoud, media) VALUES (2, 'Waar is mijn volgende stitch?', 'Ik heb een stukje al genmaakt maar ik weet niet meer zeker welke plek in moet steken met haaknaald, kan iemand me helpen?', 'stitch.jpeg')")

            # -------------------------
            # Haaktermen tabel
            # -------------------------
            cur.execute("""
                CREATE TABLE IF NOT EXISTS haaktermen (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    naam TEXT NOT NULL,
                    afkorting TEXT NOT NULL UNIQUE,
                    url TEXT
                )
            """)



            for term in haaktermen:
                cur.execute(
                    "INSERT OR IGNORE INTO haaktermen (naam, afkorting, url) VALUES (?, ?, ?)",
                    term
                )


            # -------------------------
            # Crochet Projects tabel
            # -------------------------
            cur.execute("""
                CREATE TABLE IF NOT EXISTS crochet_projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    video TEXT,
                    pattern TEXT,
                    user_id INTEGER,
                    created_at DATE DEFAULT CURRENT_DATE,
                    supplies TEXT,
                    image TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)

            # mini pets
            cur.execute("SELECT id FROM crochet_projects WHERE title = ?", ("Mini Pets with Hats",))

            if not cur.fetchone():
                pattern = """Body
R1: 6 sc in mr
R2: inc in each stitch (12)
R3: (1 sc, inc) x6 (18)
R4: (2 sc, inc) x6 (24)

R5: 8 sc, change color at 8th sc
Make a slip knot with new yarn
Attach the new yarn
Make 1 bobble stitch
(yarn over, insert, pull yarn, pull through the first 2 loops) repeat 5 times in 1 stitch
Change back to yellow yarn
5 sc, change color at the 5th stitch
Make 1 bobble stitch
(yarn over, insert, pull yarn, pull through the first 2 loops) repeat 5 times in 1 stitch
Change back to yellow yarn
9 sc
Cut the orange yarn

R6: 24 sc
R7: 24 sc

R8: 7 sc, 1 bobble stitch, 7 sc, 1 bobble stitch, 8 sc
R9: (2 sc, dec) x6 (18)
R10: (1 sc, dec) x6 (12)

Stuff the body

R11: FLO inc in each stitch (24)
R12: 24 sc
R13-17: 24 sc each round
R18: (2 sc, dec) x6 (18)

Insert the eyes between R14 and R15

R19: (1 sc, dec) x6 (12)

Stuff the head

R20: 6 dec

Leave a short yarn tail and fasten off
Sew the opening closed
Weave in the yarn end

Hat
Repeat R1–R4 of the body
3 sc, ch 1 and turn
Row 1: 21 sc, ch 1 and turn
Row 2: 21 sc, ch 1 and turn
Repeat 21 sc for 4 more rows

Make 5–6 chains
Sl st on the other end
Ch 1 and cut yarn
Weave in the ends


Beak
Embroider the beak
Secure the yarn

Ears
Make a slip knot
Ch 2
Make 5 sc in the second chain
Sl st in the same place
Ch 1 and leave a long tail for sewing

Leaf
MR
(ch 3, skip 1, sc 2, sl st) repeat 3–4 times
Ch 1, pull the tail
Leave long tail for sewing


Cat Ears
Slip knot
Ch 3
Skip 1
Sc in second chain
Ch 1
Dc in next chain
Ch 1
Sc in same place
Sl st
Ch 1 and leave long tail


Face Details
Use black yarn to embroider the face."""

                supplies = """5 ply yarn
3.5 mm crochet hook
5 mm safety eyes
Stuffing
Needle
Scissors
Stitch marker
Glue"""

                cur.execute("""
                    INSERT INTO crochet_projects
                    (title, video, pattern, user_id, created_at, supplies, image)
                    VALUES (?, ?, ?, ?, CURRENT_DATE, ?, ?)
                """, (
                    "Mini Pets with Hats",
                    "https://www.youtube.com/embed/R9bPd94XnsE",
                    pattern,
                    1,
                    supplies,
                    "mini_pets.png"
                ))

            #reversible_octopus
            cur.execute("SELECT id FROM crochet_projects WHERE title = ?", ("Reversible Octopus",))

            if not cur.fetchone():
                pattern = """R1: MR with 8 sc [8]
R2: inc x8 [16]
R3: (1 sc, inc) x8 [24]
R4: (1 sc, inc, 1 sc) x8 [32]
R5: 32 sc [32]
R6: (3 sc, inc) x8 [40]
R7-11: 40 sc [40]
R12: (3 sc, dec) x8 [32]

R13:
(2 sc, make 6 chains,
start from ch 2 make 5 sc,
dec, 1 sc) x8

R14:
(2 sc, 2 hdc, 2 dc,
[2 dc in 1 st] x2,
2 dc, 2 hdc, 2 sc) x8

Insert the safety eyes.

Make the second one using a different color of yarn:
Repeat R1–14.
Insert the safety eyes.

Use the needle to sew the two pieces together
Until you reach the last two tentacles of the octopus.

Add the stuffing.

Sew it completely closed.

Using black yarn, embroider a happy mouth on one octopus
and a sad mouth on the other."""

                supplies = """4 ply yarn (green and orange)
4–5 mm crochet hook
Fiberfill stuffing
Safety eyes
Sewing needle
Scissors
Black yarn (for embroidery)"""

                cur.execute("""
                    INSERT INTO crochet_projects
                    (title, video, pattern, user_id, created_at, supplies, image)
                    VALUES (?, ?, ?, ?, CURRENT_DATE, ?, ?)
                """, (
                    "Reversible Octopus",
                    "https://www.youtube.com/embed/usC9DkBH9oY",
                    pattern,
                    1,
                    supplies,
                    "octopus.png"
                ))

            #calabash_brothers
            cur.execute("SELECT id FROM crochet_projects WHERE title = ?", ("Calabash Brothers",))

            if not cur.fetchone():
                pattern = """R1: 6 sc in MR
R2: inc x6
R3: (sc, inc) x6
R4-6: sc around
R7: (sc, dec) x6
R8: dec x6
Add stuffing
R9: (inc) x6 in BLO
R10-11: sc around
R12: dec x4

Insert the wire.
Sew the openings closed.
Wrap the yarn around the wire.
Use a small tube and wrap the wire around the tube to shape it.

Flower:

R1: 6 sc in MR
R2: (sc, inc) x3
R3: (sc, inc, sc) x3
R4-7: sc around
R8: Change color.
(3 ch, dc, tr, 2 ch picot),
(tr, dc, 3 ch),
sl st.
Repeat 6 times.

Wrap the yarn 7–8 times around three fingers.
Use wire and wrap it around the front and back of the yarn.
Twist it tightly to secure it and trim the top ends.
Insert the wire into the flower petals and trim the top ends.
Use green yarn and wrap it around the wire.

Leaves:

R1: ch 12.
Starting from the 2nd chain from hook:
sc, 2 hdc, 4 dc, dc inc, hdc, sc, tr,
sc, hdc, dc inc, 4 dc, 2 hdc, sc.

R2: Add wire.
sc, hdc, dc, 4 dc,
(dc, 3 ch, sl st),
4 sc,
(sc, 2 ch picot, sc) x4,
(sl st, 3 ch, dc),
4 dc inc,
dc, hdc, sc.

R3:
8 sc, turn.
7 sc, sl st.
sl st to the 8th stitch on the other side,
turn, 7 sc, sl st.

Sew to secure and hide the ends.
Use green yarn and wrap it around the wire.

Attaching the tendrils:

Use green yarn and wrap about 1 cm around a new piece of wire.
Fold the wire together and wrap the yarn around the wire.
Shape it using a small tube by wrapping the wire around the tube.

Assembly:

Use green yarn and wrap about 1 cm around a new piece of wire.
Fold the wire together and wrap the yarn around the wire.

Add a leaf and wrap a few rounds of yarn to secure it.
Add the flower and wrap a few rounds.
Add the pumpkin and wrap a few rounds.

Attach the leaves, flowers, tendrils, and pumpkin in any arrangement you prefer."""

                supplies = """Small tube
Wire
Cotton yarn
2 mm crochet hook
Needle
Scissors
Stuffing"""

                cur.execute("""
                    INSERT INTO crochet_projects
                    (title, video, pattern, user_id, created_at, supplies, image)
                    VALUES (?, ?, ?, ?, CURRENT_DATE, ?, ?)
                """, (
                    "Calabash Brothers",
                    "https://www.youtube.com/embed/GU31TcyKXcU",
                    pattern,
                    1,
                    supplies,
                    "huluwa.png"
                ))

            #mochi_cat
            cur.execute("SELECT id FROM crochet_projects WHERE title = ?", ("Mochi Cat",))

            if not cur.fetchone():

                pattern = """Cat with one color pattern:
R1: 6 sc in MR [6]
R2: inc * 6 [12]
R3: (sc, inc) * 6 [18]
R4: (sc, inc, sc) * 6 [24]
R5: (3sc, inc) * 6 [30]
R6-9: sc around [30]
R10: (3sc, dec) * 6 [24]
Tail: ch * 7, from the second chain from the hook: hdc, 5slst
R11: dec, 2 sc, bo, dec, sc, dec, bo, sc, dec, sc, bo, dec, sc, dec, bo 2 sc [18]
Add stuffing
R12: (sc, dec) * 6 [12]
R13: dec * 6 [6]
Leave a medium tail, fasten off and sew the hole closed
                     
Cat ears 
Right ears:  
Ch 3, from the 2nd chain from the hook: hdc, dc, slst to R3 
Sew to secure and hide the ends 
                     
Left ear: ch 3, from the  2nd chain from the hook: hdc, dc, slst to R5 
Sew to secure and hide the ends 
                     
Face details 
Use black thread to embroider the eyes on R7, 5 stiches apart 
Embroider the nose on R8, centered between the eyes 
Embroider the wiskers 1 stitch apart from the eyes, on R7 use and R8 add blush 
Use brown yarn to make stripes on the cat 
                     
Cat with two colors pattern: 
Repeat R1 to R5 as one color cat 
R5: (3 sc, inc) * 3, (change color 2sc), sc, inc, (3 sc, inc) *2 [30] 
R6: 14 sc, (change color 4 sc), 12 sc [30] 
R7: 13 sc, (change color 6 sc), 11 sc [30] 
R8-20: follow the same pattern as R6 to R13 in the one color cat pattern, but with the another color yarn 
                     
Then embroider the face details"""

                supplies = """2mm chenille yarn
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
                    (title, video, pattern, user_id, created_at, supplies, image)
                    VALUES (?, ?, ?, ?, CURRENT_DATE, ?, ?)
                """, (
                    "Mochi Cat",
                    "https://www.youtube.com/embed/Iht1z8kpQRA",
                    pattern,
                    1,
                    supplies,
                    "mochi_cat.png"
                ))

            con.commit()

    def add_column(self, table_name: str, column_name: str, column_type: str):
        """Voeg kolom toe aan bestaande tabel als deze nog niet bestaat"""
        with self.connect() as con:
            cur = con.execute(f"PRAGMA table_info({table_name})")
            columns = [row["name"] for row in cur.fetchall()]
            if column_name not in columns:
                con.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
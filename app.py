import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from data.database import Database
from models.SQL import Queries
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "Yuan_Rou"

db = Database("data/crochet.db")
queries = Queries(db)

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'webm', 'mp3', 'wav'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def make_terms_clickable(pattern, haaktermen, project_id):
    import re
    for term_id, naam, abbrev, url in haaktermen:  # let op: voeg id toe
        for term in [abbrev, naam]:
            pattern = re.sub(
                rf'(?<!\w){re.escape(term)}(?!\w)',
                f'<a href="/term/{term_id}?project_id={project_id}">{term}</a>',
                pattern
            )
    return pattern

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def startscherm():
    return render_template('startscherm.html')

@app.route('/register', methods=['GET', 'POST'])
def registreren():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check of gebruiker al bestaat
        if queries.get_user_by_email(email):
            flash("Deze email bestaat al!", "danger")
            return redirect(url_for('startscherm'))
        else:
            # Voeg gebruiker toe
            queries.create_user(email, password)
            flash("Registratie gelukt!", "succes")
            return redirect(url_for('startscherm'))
    return render_template('registreren.html')

@app.route('/login', methods=['GET', 'POST'])
def inloggen():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = queries.login_user(email, password)
        if user:
            session['user_id'] = user['id']
            flash(f"Inloggen gelukt! Welkom {user['email']}", "success")
            return redirect(url_for('projects'))
        else:
            check = queries.email_check(email)
            if not check:
                flash("Geen account gevonden met dit e-mailadres. Maak eerst een account aan.", "warning")
            else:
                flash("Email of wachtwoord incorrect!", "danger")
    return render_template('inloggen.html')

@app.route('/project', methods=['GET', 'POST'])
def projects():
    search = request.args.get("q")

    if search:
        projects = queries.search_projects(search)
    else:
        projects = queries.get_projects()
    return render_template('project.html', projects=projects)

@app.route('/project/<int:project_id>', methods=['GET', 'POST'])
def project_detail(project_id):
    project = queries.get_project(project_id)
    terms = queries.get_terms()
    haaktermen = queries.get_haaktermen()

    pattern_text = project['pattern']
    clickable_pattern = make_terms_clickable(pattern_text, haaktermen, project_id)

    return render_template(
        "patroon.html",
        project=project,
        pattern_clickable=clickable_pattern,
        terms=terms
    )

@app.route('/term/<int:term_id>', methods=['GET', 'POST'])
def term(term_id):
    project_id = request.args.get('project_id', type=int)
    term = queries.get_term(term_id)
    return render_template(
        "haakafkorting.html",
        term=term,
        project_id=project_id
    )

@app.route('/stitch_counter/<int:project_id>', methods=['GET', 'POST'])
def stitch_counter(project_id):
    project = queries.get_project(project_id)
    return render_template("stitch_counter.html", project=project)

@app.route('/ronde_plus', methods=['GET', 'POST'])
def ronde_plus():
    session['teller'] = session.get('teller', 0) + 1
    return redirect(url_for('ronde'))

@app.route('/ronde_min', methods=['GET', 'POST'])
def ronde_min():
    teller = session.get('teller', 0)
    if teller > 0:
        session['teller'] = teller - 1
    return redirect(url_for('ronde'))

@app.route('/ronde', methods=['GET', 'POST'])
def ronde():
    teller = session.get('teller', 0)
    stitch = session.get('stitch', 0)
    return render_template('stitch_counter.html', teller=teller)

@app.route('/stitch_plus', methods=['GET', 'POST'])
def stitch_plus():
    session['stitch'] = session.get('stitch', 0) + 1
    return redirect(url_for('ronde'))

@app.route('/stitch_min', methods=['GET', 'POST'])
def stitch_min():
    stitch = session.get('stitch', 0)
    if stitch > 0:
        session['stitch'] = stitch - 1
    return redirect(url_for('ronde'))

@app.route('/questions', methods=['GET', 'POST'])
def questions():
    user_id = session.get('user_id')
    posts = queries.get_posts(user_id)
    return render_template('vragen.html', posts=posts)

@app.route('/answer/<int:post_id>', methods=['GET', 'POST'])
def answer(post_id):
    posts = queries.get_post(post_id)

    if request.method == 'POST':
        antwoord = request.form.get('antwoord')  # gebruik .get() in plaats van ['antwoord']
        foto_file = request.files.get('foto')
        video_file = request.files.get('video')
        audio_file = request.files.get('audio')

        foto_filename = None
        video_filename = None
        audio_filename = None

        if foto_file and allowed_file(foto_file.filename):
            foto_filename = secure_filename(foto_file.filename)
            foto_file.save(os.path.join(app.config['UPLOAD_FOLDER'], foto_filename))

        if video_file and allowed_file(video_file.filename):
            video_filename = secure_filename(video_file.filename)
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER'], video_filename))

        if audio_file and allowed_file(audio_file.filename):
            audio_filename = secure_filename(audio_file.filename)
            audio_file.save(os.path.join(app.config['UPLOAD_FOLDER'], audio_filename))

        user_id = session.get('user_id')
        queries.save_answer(user_id=user_id, vraag_id=post_id, tekst=antwoord, foto=foto_filename, video=video_filename, audio=audio_filename)

        return redirect(url_for('questions'))

    return render_template('beantwoorden.html', posts=posts)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        titel = request.form.get('titel')
        inhoud = request.form.get('tekst')
        user_id = session.get('user_id')
        foto_file = request.files.get('foto')

        media_filename = None
        if foto_file and foto_file.filename != '' and allowed_file(foto_file.filename):
            media_filename = secure_filename(foto_file.filename)
            foto_file.save(os.path.join(app.config['UPLOAD_FOLDER'], media_filename))

        queries.save_post(titel, inhoud, media_filename, user_id)
        return redirect(url_for('questions'))

    return render_template('maken.html')


@app.route('/mijn_overzicht', methods=['GET', 'POST'])
def mijn_overzicht():
    user_id = session.get('user_id')
    search = request.args.get("q")  # zoekterm van search bar

    if search:
        # Zoek in **alle projecten van deze gebruiker** op titel of pattern
        ontwerpen = queries.search_projects(user_id, search)
    else:
        # Alles van deze gebruiker
        ontwerpen = queries.get_ontwerpen(user_id)

    return render_template('mijn_overzicht.html', ontwerpen=ontwerpen)

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        # Form data ophalen
        user_id = session.get('user_id')
        title = request.form.get('title')
        pattern = request.form.get('pattern')
        supplies = request.form.get('supplies')

        image_file = request.files.get('image')
        video_file = request.files.get('video')

        image_name = None
        video_name = None

        UPLOAD_FOLDER = 'static/uploads'

        # Afbeelding opslaan
        if image_file and allowed_file(image_file.filename):
            image_name = secure_filename(image_file.filename)
            image_file.save(os.path.join(UPLOAD_FOLDER, image_name))

        # Video opslaan
        if video_file and allowed_file(video_file.filename):
            video_name = secure_filename(video_file.filename)
            video_file.save(os.path.join(UPLOAD_FOLDER, video_name))

        # Opslaan in database via je Queries klasse
        queries.insert_project(
            user_id=user_id,
            title=title,
            pattern=pattern,
            supplies=supplies,
            image=image_name,
            video=video_name
        )

        return redirect(url_for('projects'))

    # GET request → toon formulier
    return render_template('new.html')

@app.route('/supplies/<int:project_id>')
def supplies(project_id):

    project = queries.get_project(project_id)

    return render_template(
        'supplies.html',
        project=project
    )

@app.route('/vragenoverzicht')
def vragenoverzicht():
    user_id = session.get('user_id')
    posts = queries.my_questions(user_id)
    return render_template('vragenoverzicht.html', posts=posts)

@app.route('/geantwoord/<int:post_id>', methods=['GET', 'POST'])
def geantwoord(post_id):
    post = queries.get_post(post_id)
    answers = queries.answer_people(post_id)  # haal antwoorden van andere gebruikers
    return render_template('antwoorden.html', posts=post, answers=answers)

if __name__ == '__main__':
    app.run(debug=True)

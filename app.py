from flask import Flask, render_template, request, redirect, url_for, session
from data.database import Database
from models.SQL import Queries

app = Flask(__name__)
app.secret_key = "Yuan_Rou"

db = Database("data/crochet.db")
queries = Queries(db)

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
    projects = queries.get_projects()
    return render_template('project.html', projects=projects)

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

@app.route('/project/<int:project_id>')
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

@app.route('/term/<int:term_id>')
def term(term_id):
    project_id = request.args.get('project_id', type=int)
    term = queries.get_term(term_id)
    return render_template(
        "haakafkorting.html",
        term=term,
        project_id=project_id
    )

@app.route('/stitch_counter/<int:project_id>')
def stitch_counter(project_id):
    project = queries.get_project(project_id)
    return render_template("stitch_counter.html", project=project)

@app.route('/ronde_plus')
def ronde_plus():
    session['teller'] = session.get('teller', 0) + 1
    return redirect(url_for('ronde'))

@app.route('/ronde_min')
def ronde_min():
    teller = session.get('teller', 0)
    if teller > 0:
        session['teller'] = teller - 1
    return redirect(url_for('ronde'))

@app.route('/ronde')
def ronde():
    teller = session.get('teller', 0)
    stitch = session.get('stitch', 0)
    return render_template('stitch_counter.html', teller=teller)

@app.route('/stitch_plus')
def stitch_plus():
    session['stitch'] = session.get('stitch', 0) + 1
    return redirect(url_for('ronde'))

@app.route('/stitch_min')
def stitch_min():
    stitch = session.get('stitch', 0)
    if stitch > 0:
        session['stitch'] = stitch - 1
    return redirect(url_for('ronde'))

if __name__ == '__main__':
    app.run(debug=True)

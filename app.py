from flask import Flask, render_template, request, redirect, url_for, flash
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
            return redirect(url_for('startscherm'))
        else:
            check = queries.email_check(email)
            if not check:
                flash("Geen account gevonden met dit e-mailadres. Maak eerst een account aan.", "warning")
            else:
                flash("Email of wachtwoord incorrect!", "danger")
    return render_template('inloggen.html')

if __name__ == '__main__':
    app.run(debug=True)

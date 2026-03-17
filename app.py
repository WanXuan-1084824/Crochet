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
            flash("Deze email bestaat al!")
            return redirect(url_for('startscherm'))
        else:
            # Voeg gebruiker toe
            queries.create_user(email, password)
            flash("Registratie gelukt!")
            return redirect(url_for('startscherm'))
    return render_template('registreren.html')

if __name__ == '__main__':
    app.run(debug=True)

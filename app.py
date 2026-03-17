from flask import Flask, render_template
from data.database import Database
from models.SQL import Queries

app = Flask(__name__)


db = Database("data/crochet.db")
queries = Queries(db)

@app.route('/', methods=['GET', 'POST'])
def startscherm():
    return render_template('startscherm.html')

@app.route('/register', methods=['GET', 'POST'])
def registreren():
    return render_template('registreren.html')

if __name__ == '__main__':
    app.run(debug=True)

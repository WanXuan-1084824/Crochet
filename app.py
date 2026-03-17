from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def startscherm():
    return render_template('startscherm.html')

@app.route('/register', methods=['GET', 'POST'])
def registreren():
    return render_template('registreren.html')

if __name__ == '__main__':
    app.run(debug=True)

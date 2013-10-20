from flask import Flask, render_template, request, redirect, url_for, session, flash, g, jsonify
from functools import wraps
import sqlite3

DATABASE = 'red.db'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'mi preciosa'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def home():
    return render_template('home.html')

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to login first.')
            return redirect(url_for('log'))
    return wrap

@app.route('/hello')
@login_required
def hello():
    g.db = connect_db()
    cur = g.db.execute('select nombre from carrera')
    carreras = [dict(nombre=row[0])for row in cur.fetchall()]
    g.db.close()
    return render_template('hello.html', carreras=carreras)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash("You wew logged out")
    return redirect(url_for('log'))

@app.route('/login', methods=['GET', 'POST'])
def log():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again'
        else:
            session['logged_in'] = True
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)

@app.route('/perfil')
def get_current_user():
    g.db = connect_db()
    cur = g.db.execute('select id, username, carrera, turno, ciclo from usuario')
    usuario = [dict(id=row[0], nombre=row[1], carrera=row[2], turno=row[3], ciclo=row[4])for row in cur.fetchall()]
    g.db.close()
    return jsonify(username=usuario[0].get('nombre', None),
                   carrera=usuario[0].get('carrera', None),
                   turno=usuario[0].get('turno', None),
                   ciclo=usuario[0].get('ciclo', None)
                   )


@app.route('/carrera')
def get_current_carreras():
    return jsonify(username='jo',
                   email='aa',
                   id='1')


@app.route('/turno')
def get_current_turno():
    return jsonify(username='jo',
                   email='aa',
                   id='1')


@app.route('/profesor')
def get_current_profesor():
    return jsonify(username='jo',
                   email='aa',
                   id='1')

if __name__ == "__main__":
    app.run(debug=True)

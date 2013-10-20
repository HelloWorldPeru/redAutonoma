from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, json
import connection as cn
import resolve as rs
from functools import wraps

app = cn.app

#WebPage

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
    cn.g.db = cn.connect_db()
    cur = cn.g.db.execute('select nombre from carrera')
    carreras = [dict(nombre=row[0])for row in cur.fetchall()]
    cn.g.db.close()
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

#APP Phonegap

@app.route('/login-ajax', methods=['POST'])
def login_ajax():
    error = None
    result = {}
    if request.method == 'POST':
        result = rs.check_login(request.form['username'], request.form['password'] )
    return json.dumps(result)


@app.route('/perfil/<int:user_token>')
def get_current_user(user_token):
    try:
        if user_token is not None:
            data = {}
            cn.g.db = cn.connect_db()
            cur = cn.g.db.execute('select id, username, carrera, turno, ciclo from usuario where token='+str(user_token))
            usuario = [dict(id=row[0], nombre=row[1], carrera=row[2], turno=row[3], ciclo=row[4])for row in cur.fetchall()]
            for user in usuario:
                data.update({
                    'id':user.get('id'),
                    'username':user.get('nombre'),
                    'carrera':rs.get_carrera(user.get('carrera')),
                    'turno':rs.get_turno(user.get('turno')),
                    'ciclo':user.get('ciclo')
                })

            cn.g.db.close()
            return json.dumps(data)
        else:
            return jsonify(message='Error query')
    except:
        return jsonify(message='Error query')


@app.route('/carrera')
def get_current_carreras():
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute('select id, nombre from carrera')
        carreras = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
        cn.g.db.close()
        return json.dumps(carreras)
    except:
        return jsonify(message='Error query')


@app.route('/turno')
def get_current_turno():
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute('select id, nombre from turno')
        carreras = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
        cn.g.db.close()
        return json.dumps(carreras)
    except:
        return jsonify(message='Error query')


@app.route('/profesor')
def get_current_profesor():
    return jsonify(username='jo',
                   email='aa',
                   id='1')

if __name__ == "__main__":
    app.run(debug=True)

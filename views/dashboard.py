from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, json
import connection as cn
from functools import wraps


def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to login first.')
            return redirect(url_for('login'))
    return wrap


@login_required
def dashboard():
    return render_template('dashboard.html')

@login_required
def carreras():
    cn.g.db = cn.connect_db()
    cur = cn.g.db.execute('select id, nombre from carrera')
    carreras = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
    cn.g.db.close()
    return render_template('admin/carrera.html', carreras=carreras)

@login_required
def criterios():
    cn.g.db = cn.connect_db()
    cur = cn.g.db.execute('select id, nombre from criterios')
    criterios = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
    cn.g.db.close()
    return render_template('admin/criterios.html', criterios=criterios)

@login_required
def profesores():
    cn.g.db = cn.connect_db()
    cur = cn.g.db.execute('select id, nombre from profesor')
    profesores = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
    cn.g.db.close()
    return render_template('admin/profesor.html', profesores=profesores)

@login_required
def turnos():
    cn.g.db = cn.connect_db()
    cur = cn.g.db.execute('select id, nombre from turno')
    turnos = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
    cn.g.db.close()
    return render_template('admin/turno.html', turnos=turnos)

@login_required
def usuarios():
    cn.g.db = cn.connect_db()
    cur = cn.g.db.execute('select id, username, carrera, turno, ciclo, seccion from usuario')
    usuarios = [dict(id=row[0], nombre=row[1], carrera=row[2], turno=row[3], ciclo=row[4], seccion=row[5])for row in cur.fetchall()]
    cn.g.db.close()
    return render_template('admin/usuario.html', usuarios=usuarios)

from flask import render_template,redirect, url_for, session, flash
import connection as cn
from functools import wraps
import resolve as rs


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
def cursos():
    cn.g.db = cn.connect_db()
    cur = cn.g.db.execute('Select cu.id, cu.nombre, ca.nombre, t.nombre, cu.ciclo, p.nombre, cu.seccion, cu.dia from curso cu inner join carrera ca on cu.carrera = ca.id inner join turno t on t.id = cu.turno inner join profesor p on p.id = cu.profesor')
    cursos = [dict(id=row[0], nombre=row[1], carrera=row[2], turno=row[3], ciclo=row[4], profesor=row[5], seccion=row[6], dia=row[7])for row in cur.fetchall()]
    cn.g.db.close()
    return render_template('admin/cursos.html', cursos=cursos)

@login_required
def usuarios():
    cn.g.db = cn.connect_db()
    cur = cn.g.db.execute('select u.id, u.username,c. nombre,t. nombre,u. ciclo,u. seccion, u.token from usuario u inner join carrera c on c.id = u.carrera inner join turno t on t.id = u.turno')
    usuarios = [dict(id=row[0], nombre=row[1], carrera=row[2], turno=row[3], ciclo=row[4], seccion=row[5], token=row[6])for row in cur.fetchall()]
    cn.g.db.close()
    return render_template('admin/usuario.html', usuarios=usuarios)


@login_required
def detale_usuario(token_user):
    dias = [1,2,3,4,5]
    detalles = []
    profile = rs.get_profile(token_user)
    for dia in dias:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute("select c.id, c.nombre, p.nombre from curso c inner join profesor p on p.id=c.profesor where carrera="+profile.get('carrera')+" and turno="+profile.get('turno')+" and ciclo="+profile.get('ciclo')+" and dia="+str(dia)+" and seccion='"+profile.get('seccion')+"'")
        cursos = [dict(id=row[0], nombre=row[1], profesor=row[2])for row in cur.fetchall()]
        if len(cursos) > 0:
            cursos[0].update({'dia':str(dia)})
            detalles.append(cursos[0])
        cn.g.db.close()
    return render_template('admin/detalles_user.html', detalles=detalles)

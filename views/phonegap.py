from flask import request,jsonify, json
from flask import make_response, request, current_app
from datetime import timedelta
import datetime
import connection as cn
import resolve as rs
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


@crossdomain(origin='*')
def login_ajax():
    error = None
    result = {}
    if request.method == 'POST':
        result = rs.check_login(request.form['username'], request.form['password'] )
    return json.dumps(result)


@crossdomain(origin='*')
def update_information():
    error = None
    result = {}
    if request.method == 'POST':
        try:
            cn.g.db = cn.connect_db()
            cn.g.db.execute("update usuario set carrera="+str(request.form['carrera'])+",turno="+str(request.form['turno'])+",ciclo="+str(request.form['ciclo'])+" where token='"+str(request.form['token'])+"'")
            cn.g.db.commit()
            result = {'status':True}
        except:
            result = {'status':False}
    return json.dumps(result)


@crossdomain(origin='*')
def get_current_user():
    if request.method == 'POST':
        try:
            user_token = request.form['token']
            if user_token is not None:
                data = {}
                cn.g.db = cn.connect_db()
                cur = cn.g.db.execute('select id, username, carrera, turno, ciclo, seccion from usuario where token='+str(user_token))
                usuario = [dict(id=row[0], nombre=row[1], carrera=row[2], turno=row[3], ciclo=row[4], seccion=row[5])for row in cur.fetchall()]
                for user in usuario:
                    data.update({
                        'id':user.get('id'),
                        'username':user.get('nombre'),
                        'carrera':rs.get_carrera(user.get('carrera')),
                        'turno':rs.get_turno(user.get('turno')),
                        'ciclo':user.get('ciclo'),
                        'seccion':user.get('seccion')
                    })

                cn.g.db.close()
                return json.dumps(data)
            else:
                return jsonify(message='Error query')
        except:
            return jsonify(message='Error query')


@crossdomain(origin='*')
def get_current_carreras():
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute('select id, nombre from carrera')
        carreras = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
        cn.g.db.close()
        return json.dumps(carreras)
    except:
        return jsonify(message='Error query')


@crossdomain(origin='*')
def get_current_turno():
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute('select id, nombre from turno')
        carreras = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
        cn.g.db.close()
        return json.dumps(carreras)
    except:
        return jsonify(message='Error query')


@crossdomain(origin='*')
def get_curso():
    try:
        if request.method == 'POST':
            user_token = request.form['token']
            if user_token is not None:
                data = {}
                profile = rs.get_profile(user_token)
                dia = datetime.datetime.today().weekday() + 1
                cn.g.db = cn.connect_db()
                cur = cn.g.db.execute("select c.id, c.nombre, p.nombre from curso c inner join profesor p on p.id=c.profesor where carrera="+profile.get('carrera')+" and turno="+profile.get('turno')+" and ciclo="+profile.get('ciclo')+" and dia="+str(dia)+" and seccion='"+profile.get('seccion')+"'")
                usuario = [dict(id_curso=row[0], curso=row[1], profesor=row[2])for row in cur.fetchall()]
                for user in usuario:
                    data.update({
                        'id':user.get('id_curso'),
                        'curso':user.get('curso'),
                        'profesor':user.get('profesor')
                    })
                cn.g.db.close()
                return json.dumps(data)
            else:
                return jsonify(message='Error query')
    except:
        return jsonify(message='Error query')


@crossdomain(origin='*')
def get_criterios():
    cn.g.db = cn.connect_db()
    cur = cn.g.db.execute('select id, nombre from criterios')
    criterios = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
    cn.g.db.close()
    return json.dumps(criterios)


@crossdomain(origin='*')
def calificar_curso():
    try:
        if request.method == 'POST':
            user_token = request.form['token']
            curso = request.form['curso']
            calificaciones =  json.loads( request.form['califica'])
            fecha = datetime.datetime.today().strftime('%d/%m/%Y')
            profile = rs.get_profile(user_token)

            if user_token is not None:
                option = 'UPDATE'
                evaluation = rs.get_evaluation(fecha,curso)
                if evaluation is None:
                    rs.save_evaluation(fecha,curso)
                    evaluation = rs.get_evaluation(fecha,curso)

                calificacion = rs.get_calificacion(profile.get('id'),evaluation)
                if calificacion is None:
                    option = 'SAVE'

                for calificacion in calificaciones:
                    rs.save_calificacion(option, profile.get('id'),evaluation, calificacion.get('id'),calificacion.get('valor'))
                data = {
                    'status':200
                }
                return json.dumps(data)
            else:
                return jsonify(message='Error query')
    except:
        return jsonify(message='Error query')

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, json
import connection as cn
import resolve as rs


def login_ajax():
    error = None
    result = {}
    if request.method == 'POST':
        result = rs.check_login(request.form['username'], request.form['password'] )
    return json.dumps(result)


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


def get_current_carreras():
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute('select id, nombre from carrera')
        carreras = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
        cn.g.db.close()
        return json.dumps(carreras)
    except:
        return jsonify(message='Error query')


def get_current_turno():
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute('select id, nombre from turno')
        carreras = [dict(id=row[0], nombre=row[1])for row in cur.fetchall()]
        cn.g.db.close()
        return json.dumps(carreras)
    except:
        return jsonify(message='Error query')


def get_curso(user_token):
    try:
        if user_token is not None:
            data = {}
            cn.g.db = cn.connect_db()
            cur = cn.g.db.execute('select id, nombre from curso where carrera=?, turno=?, ciclo=?, dia=?')
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

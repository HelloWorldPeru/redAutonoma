import connection as cn


def get_carrera(id_carrera, json=True):
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute('select nombre from carrera where id='+str(id_carrera))
        carrera = [dict(nombre=row[0])for row in cur.fetchall()]
        cn.g.db.close()
        if json:
            return {'id':id_carrera, 'nombre':carrera[0].get('nombre')}
        else:
            return carrera[0].get('nombre')
    except:
        return {'id':id_carrera, 'nombre':'Ninguna'}


def get_turno(id_turno, json=True):
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute('select nombre from turno where id='+str(id_turno))
        carrera = [dict(nombre=row[0])for row in cur.fetchall()]
        cn.g.db.close()
        if json:
            return {'id':id_turno, 'nombre':carrera[0].get('nombre')}
        else:
            return carrera[0].get('nombre')
    except:
        return {'id':id_turno, 'nombre':'Ninguna'}


def check_login(username, password):
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute("select token from usuario where username='"+str(username)+"' and password='"+str(password)+"'")
        token = [dict(clave=row[0])for row in cur.fetchall()]
        cn.g.db.close()
        if len(token) > 0:
            return {
                'status': True,
                'message':'Welcome',
                'token':token[0].get('clave')

            }
        else:
            return {
                'status': False,
                'message':'Login incorrect'
            }
    except:
        return {}
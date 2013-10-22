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


def get_profile(token_user):
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute('select carrera, turno, ciclo, seccion, id from usuario where token='+str(token_user))
        usuario = [dict(carrera=row[0], turno=row[1], ciclo=row[2], seccion=row[3], id=row[4])for row in cur.fetchall()]
        cn.g.db.close()
        return {
            'carrera':str(usuario[0].get('carrera')),
            'turno':str(usuario[0].get('turno')),
            'ciclo':str(usuario[0].get('ciclo')),
            'seccion':str(usuario[0].get('seccion')),
            'id':str(usuario[0].get('id'))
        }
    except:
        return {}


def save_evaluation(fecha,curso):
    try:
        cn.g.db = cn.connect_db()
        cn.g.db.execute("insert into evaluacion(fecha, total, curso) values('"+fecha+"',0,"+curso+")")
        cn.g.db.commit()
        return True
    except:
        return False


def get_evaluation(fecha,curso):
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute("select id from evaluacion where fecha='"+str(fecha)+"' and curso="+str(curso))
        evaluacion = [dict(id=row[0])for row in cur.fetchall()]
        cn.g.db.close()
        if(len(evaluacion)>0):
            return evaluacion[0].get('id')
        return None
    except:
        return None


def save_calificacion(option, usuario,evaluacion, criterio, valor):
    try:
        cn.g.db = cn.connect_db()
        if option == 'SAVE':
            cn.g.db.execute("insert into calificacion(usuario, evaluacion, criterio, valor) values("+str(usuario)+","+str(evaluacion)+","+str(criterio)+","+str(valor)+")")
        elif option == 'UPDATE':
            cn.g.db.execute("update calificacion set valor="+str(valor)+" where usuario="+str(usuario)+" and evaluacion="+str(evaluacion)+" and criterio="+str(criterio))
        cn.g.db.commit()
        return True
    except:
        return False


def get_calificacion(usuario,evaluacion):
    try:
        cn.g.db = cn.connect_db()
        cur = cn.g.db.execute("select id from calificacion where usuario="+str(usuario)+" and evaluacion="+str(evaluacion))
        evaluacion = [dict(id=row[0])for row in cur.fetchall()]
        cn.g.db.close()
        if(len(evaluacion)>0):
            return evaluacion[0].get('id')
        return None
    except:
        return None
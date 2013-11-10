import sqlite3 as lite
import sys

# usuarios = (
#     ('jonathancg90','321','321',1,1,6)
# )
con = lite.connect('red.db')

with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS criterios")
    cur.execute("CREATE TABLE criterios("
                "id integer primary key autoincrement,"
                "nombre TEXT"
                ")")
    cur.execute("INSERT INTO criterios (nombre) VALUES('Felicidad')")
    cur.execute("INSERT INTO criterios (nombre) VALUES('Descanso')")
    cur.execute("INSERT INTO criterios (nombre) VALUES('Item')")
    cur.execute("INSERT INTO criterios (nombre) VALUES('Otro item')")

    cur.execute("DROP TABLE IF EXISTS carrera")
    cur.execute("CREATE TABLE carrera("
                "id integer primary key autoincrement,"
                "nombre TEXT"
                ")")
    cur.execute("INSERT INTO carrera (nombre) VALUES('Ing. Sistemas')")

    cur.execute("DROP TABLE IF EXISTS turno")
    cur.execute("CREATE TABLE turno("
                "id integer primary key autoincrement,"
                "nombre TEXT"
                ")")
    cur.execute("INSERT INTO turno(nombre) VALUES('Diurno')")
    cur.execute("INSERT INTO turno(nombre) VALUES('Tarde')")
    cur.execute("INSERT INTO turno(nombre) VALUES('Noche')")

    cur.execute("DROP TABLE IF EXISTS profesor")
    cur.execute("CREATE TABLE profesor("
                "id integer primary key autoincrement,"
                "nombre TEXT"
                ")")
    cur.execute("INSERT INTO profesor (nombre) VALUES('SIXTO CORDOVA CASTRO')")
    cur.execute("INSERT INTO profesor (nombre) VALUES('CARLOS RUBEN GUERRERO MONCADA')")
    cur.execute("INSERT INTO profesor (nombre) VALUES('LELLY VALEZZA BERMUDEZ TAPIA')")
    cur.execute("INSERT INTO profesor (nombre) VALUES('SEGUNDO ZOILO VASQUEZ RUIZ')")
    cur.execute("INSERT INTO profesor (nombre) VALUES('IVAN CRISPIN SANCHEZ')")

    cur.execute("INSERT INTO profesor (nombre) VALUES('Profesor Jirafales')")

    cur.execute("DROP TABLE IF EXISTS curso")
    cur.execute("CREATE TABLE curso("
                "id integer primary key autoincrement,"
                "nombre TEXT,"
                "carrera INT,"
                "turno INT,"
                "ciclo INT,"
                "profesor INT,"
                "seccion TEXT,"
                "dia INT,"
                "FOREIGN KEY(carrera) REFERENCES carrera(id),"
                "FOREIGN KEY(turno) REFERENCES turno(id),"
                "FOREIGN KEY(profesor) REFERENCES profesor(id)"
                ")")
    cur.execute("INSERT INTO curso (nombre, carrera, turno, ciclo, profesor,seccion, dia) VALUES('SISTEMAS OPERATIVOS',1,1,6,1,'A',1)")
    cur.execute("INSERT INTO curso (nombre, carrera, turno, ciclo, profesor,seccion, dia) VALUES('MODELAMIENTO Y SIMULACION',1,1,6,2,'A',2)")
    cur.execute("INSERT INTO curso (nombre, carrera, turno, ciclo, profesor,seccion, dia) VALUES('CONSTITUCION Y DERECHOS HUMANOS',1,1,6,3,'A',3)")
    cur.execute("INSERT INTO curso (nombre, carrera, turno, ciclo, profesor,seccion, dia) VALUES('INGENIERIA EMPRESARIAL',1,1,6,4,'A',4)")
    cur.execute("INSERT INTO curso (nombre, carrera, turno, ciclo, profesor,seccion, dia) VALUES('INGENIERIA DE LA INFORMACION',1,1,6,5,'A',5)")

    cur.execute("INSERT INTO curso (nombre, carrera, turno, ciclo, profesor,seccion, dia) VALUES('INGENIERIA DE LOS SABADOS',1,1,6,6,'A',6)")
    cur.execute("INSERT INTO curso (nombre, carrera, turno, ciclo, profesor,seccion, dia) VALUES('INGENIERIA DE LOS DOMINGOS',1,1,6,6,'A',7)")

    cur.execute("INSERT INTO curso (nombre, carrera, turno, ciclo, profesor,seccion, dia) VALUES('Sistemas OPerativos',1,1,6,1,'B',1)")

    cur.execute("DROP TABLE IF EXISTS usuario")
    cur.execute("CREATE TABLE usuario("
                "id integer primary key autoincrement,"
                "username TEXT,"
                "nombre TEXT,"
                "password TEXT,"
                "token TEXT,"
                "carrera INT,"
                "turno INT,"
                "ciclo INT,"
                "seccion TEXT"
                ")")

    cur.execute("INSERT INTO usuario (username, nombre, password, token, carrera, turno, ciclo, seccion) VALUES('jonathancg90', 'Jonathan', '123456','13233',1,1,6,'A')")
    cur.execute("INSERT INTO usuario (username, nombre, password, token, carrera, turno, ciclo, seccion) VALUES('tectime', 'John', '654321','14433',1,1,6, 'B')")

    cur.execute("DROP TABLE IF EXISTS evaluacion")
    cur.execute("CREATE TABLE evaluacion("
                "id integer primary key autoincrement,"
                "fecha DATE,"
                "Total INT,"
                "curso INT,"
                "FOREIGN KEY(curso) REFERENCES curso(id)"
                ")")

    cur.execute("DROP TABLE IF EXISTS calificacion")
    cur.execute("CREATE TABLE calificacion("
                "evaluacion INT,"
                "id integer primary key autoincrement,"
                "usuario TEXT,"
                "criterio INTEGER,"
                "valor INT,"
                "FOREIGN KEY(criterio) REFERENCES criterio(id),"
                "FOREIGN KEY(usuario) REFERENCES usuario(id)"
                ")")

    # cur.executemany("INSERT INTO usuario(username, password, token, carrera, turno, ciclo) VALUES(?,?,?,?,?,?)", usuarios)
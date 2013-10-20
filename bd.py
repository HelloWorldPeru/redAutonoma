import sqlite3 as lite
import sys

# usuarios = (
#     ('jonathancg90','321','321',1,1,6)
# )
con = lite.connect('red.db')

with con:
    cur = con.cursor()


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
    cur.execute("INSERT INTO profesor (nombre) VALUES('Tectime')")

    cur.execute("DROP TABLE IF EXISTS curso")
    cur.execute("CREATE TABLE curso("
                "id integer primary key autoincrement,"
                "nombre TEXT,"
                "carrera INT,"
                "turno INT,"
                "ciclo INT,"
                "profesor INT,"
                "dia INT,"
                "FOREIGN KEY(carrera) REFERENCES carrera(id),"
                "FOREIGN KEY(turno) REFERENCES turno(id),"
                "FOREIGN KEY(profesor) REFERENCES profesor(id)"
                ")")
    cur.execute("INSERT INTO curso (nombre, carrera, turno, ciclo, profesor, dia) VALUES('Derecho y constitucion',1,1,6,1,1)")

    cur.execute("DROP TABLE IF EXISTS usuario")
    cur.execute("CREATE TABLE usuario("
                "id integer primary key autoincrement,"
                "username TEXT,"
                "password TEXT,"
                "token TEXT,"
                "carrera INT,"
                "turno INT,"
                "ciclo INT"
                ")")

    cur.execute("INSERT INTO usuario (username, password, token, carrera, turno, ciclo) VALUES('jonathancg90','123456','13233',1,1,6)")

    # cur.executemany("INSERT INTO usuario(username, password, token, carrera, turno, ciclo) VALUES(?,?,?,?,?,?)", usuarios)
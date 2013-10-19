import sqlite3 as lite
import sys

sales = (
    ('jonathan', 22000),
    ('jose', 21000),
    ('Ana', 2000),
    ('Diana', 22400),
    ('Hubert', 22060)
)

con = lite.connect('sales.db')

with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS reps")
    cur.execute("CREATE TABLE reps(rep_name TEX, amount INT)")
    cur.executemany("INSERT INTO reps VALUES(?, ?)", sales)
from flask import Flask, g
import sqlite3

DATABASE = 'red.db'

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'mi preciosa'


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
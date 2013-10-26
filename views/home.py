from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, json
import connection as cn
import resolve as rs
from functools import wraps


def index():
    return render_template('home.html')


def logout():
    session.pop('logged_in', None)
    flash("You wew logged out")
    return redirect(url_for('log'))


def log():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again'
        else:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
    return render_template('login.html', error=error)

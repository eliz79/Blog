#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Author - Erica Liz

from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3

app = Flask(__name__)
app.secret_key = 'a secret key'
app.database = 'sample.db'

# login required decorator
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Enter username and password.')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@login_required
def home():
    g.db = connect_db()
    cur = g.db.execute('select * from posts')
    posts = [dict(title=row[0], description=row[1]) for row in cur.fetchall()]
    g.db.close()
    return render_template('index.html', posts=posts)  # render a template
    
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'test' or request.form['password'] != 'test':
            error = 'Invalid username/password. Please try again.'
        else:
            session['logged_in'] = True
            flash('You are logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/comments')
@login_required
def comments():
    return render_template('comments.html')

@app.route('/new', methods=['GET'])
@login_required
def new_comment():
    if request.method == 'GET':
            return render_template('feedback.html')
    
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You are logged out!')
    return redirect(url_for('welcome'))

def connect_db():
    return sqlite3.connect(app.database)


if __name__ == '__main__':
    app.run()

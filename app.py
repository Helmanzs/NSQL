import os
from flask import Flask, render_template, request, url_for, redirect, session
from databaseClient import Database
from populate_database import populate_db
import logging
import sys

app = Flask(__name__)
db = Database('mongodb://admin:admin@mongo:27017', app)
polls = []
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/')
def index():
    polls = db.getPolls()
    if polls == 0:
        return render_template('empty.html')
    
    if 'User' in session:
        for poll in polls:
            if session['User']['username'] in poll['users']:
                poll['disabled'] = True
            elif session['User']['username'] == poll['user']:
                poll['own'] = True
            else:
                poll['disabled'] = False
                poll['own'] = False
    else:
        for poll in polls:
            poll['viewer'] = True

    return render_template('index.html', polls=polls)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        result = db.register(request.form['username'], request.form['password'], request.form['email'])
        if result == 1:
            return redirect(url_for('index'))
        else:
            return render_template('register.html', failed=True)

    return render_template('register.html', failed=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.method)
    if request.method == 'POST':
        result = db.login(request.form['username'], request.form['password'])
        if result == 1:
            return redirect(url_for('index'))
        else:
            return render_template('login.html', failed=True)
        
    return render_template('login.html', failed=True)

@app.route('/vote', methods=['POST'])
def vote():
    result = db.vote(int(request.form['idx']), int(request.form['options']))
    if result == 1:
        return redirect(url_for('index', vote_failed=False))
    else:
        return redirect(url_for('index', vote_failed=True))

@app.route('/logout', methods=['POST'])
def logout():
    db.logout()
    return redirect(url_for('index'))

@app.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if not session.get('User'):
        return render_template('login.html')
    
    return render_template('create_poll.html')

@app.route('/submit_poll', methods=['POST'])
def submit_poll():
    db.submit_poll(request.form['question'], request.form.getlist('option[]'))
    return redirect(url_for('index'))

@app.route('/delete_all')
def delete_all():
    return db.delete_all()

@app.route('/populate')
def populate():
    populate_db(db)
    return redirect(url_for('index'))
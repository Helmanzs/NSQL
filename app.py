from flask import Flask, jsonify, render_template, request, url_for, redirect, session
from databaseClient import Database

app = Flask(__name__)
app.secret_key = "kek"
db = Database('mongodb://admin:admin@mongo:27017')
polls = []

'''polls = [
  {
    "question": "Favorite Color Poll",
    "options": ["Red", "Blue", "Green"],
    "votes": [3, 0, 4],
    "user": "admin",
    "users": []
  },
  {
    "question": "Weekend Activity Poll",
    "options": ["Hiking", "Reading", "Watching Movies"],
    "votes": [1, 2, 3],
    "user": "user2",
    "users": []
  },
  {
    "question": "Programming Language Poll",
    "options": ["Python", "Java", "JavaScript", "C++"],
    "votes": [1, 0, 0, 0],
    "user": "user3",
    "users": ['admin']
  }
]'''


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
        print(result)
        if result == 1:
            return redirect(url_for('index'))
        else:
            return render_template('register.html', failed=True)

    return render_template('register.html', failed=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
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


@app.route('/debug')
def debug():
    users = list(db.users.find({}, {"_id": 0}))
    return users

@app.route('/delete_all_polls')
def delete_all_polls():
    return db.delete_polls()
    
if __name__ == '__main__':
    app.run()

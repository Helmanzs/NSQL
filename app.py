from flask import Flask, jsonify, render_template, request, url_for, redirect, session
from pymongo import MongoClient, errors
from user import User
from poll import Poll
from datetime import datetime

app = Flask(__name__)
app.secret_key = "kek"
client = MongoClient('mongodb://admin:admin@mongo:27017')
db = client.get_database('NSQL')
polls = [
    {
        "question": "What is your favorite color?",
        "options": ["Red", "Blue", "Green"],
        "votes": [0, 0, 0],
        "user": "admin",
        "users": ["user456"]
    },
    {
        "question": "Which programming language do you prefer?",
        "options": ["Python", "Java", "JavaScript"],
        "votes": [0, 0, 0],
        "user": "admin2",
        "users": ["user101", "user202"]
    },
    # Additional documents...
]

@app.route('/')
def index():
    #polls = list(db.polls.find({}, {"_id": 0}))
    
    return render_template('index.html', polls=polls)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if not db.users.find_one({'username': username}):
            user = User(username, password, email)
            db.users.insert_one({'username': user.username, 'password': user.password, 'email': user.email})
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_data = db.users.find_one({'username': username})

        if user_data and User.check_password(user_data['password'], password):
            user = User(username, password, user_data['email'])
            session['User'] = User.to_json(user)
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/vote', methods=['POST'])
def vote():
    user = session['User']['username']
    index = int(request.form['idx'])
    option = int(request.form['options'])
    poll = polls[index]
    votes = poll['votes']
    if user != poll['user']:
        votes[option] += 1
    print(votes)
    return redirect(url_for('index'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/create_poll', methods=['GET', 'POST'])
def create_poll():
    if not session.get('User'):
        return render_template('login.html')
    
    return render_template('create_poll.html')

@app.route('/submit_poll', methods=['POST'])
def submit_poll():
   # Get form data
    question = request.form['question']
    options = request.form.getlist('option[]')
    user = User.from_json(session['User'])
    poll = Poll(question=question, options=options, user=user)
    db.polls.insert_one({'user': user.username, 'question': poll.question, 'options': poll.options, 'votes': poll.votes, 'date_added': datetime.now()})
    return redirect(url_for('index'))


@app.route('/debug')
def debug():
    users = list(db.users.find({}, {"_id": 0}))
    return users

if __name__ == '__main__':
    app.run()

def ping_db():
    try:
        client.server_info() 
        return jsonify({'status': 'success', 'message': 'Database connection successful'})
    except errors.ServerSelectionTimeoutError as e:
        return jsonify({'status': 'error', 'message': 'Failed to connect to the database'})


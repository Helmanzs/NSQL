from flask import Flask, jsonify, render_template, request, url_for, redirect, session
from pymongo import MongoClient, errors
from user import User
from poll import Poll

app = Flask(__name__)
app.secret_key = "kek"
client = MongoClient('mongodb://admin:admin@mongo:27017')
db = client.get_database('NSQL')
polls = [
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
]


@app.route('/')
def index():
    #polls = list(db.polls.find({}))
    if(len(polls) > 0):
        for poll in polls:
            if session['User']['username'] in poll['users']:
                poll['disabled'] = True
            elif session['User']['username'] == poll['user']:
                poll['own'] = True
            else:
                poll['disabled'] = False
                poll['own'] = False
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
    poll = polls[index]
    option = int(request.form['options'])
    votes = poll['votes']
    if user != poll['user']:
        votes[option] += 1
        poll['users'].append(user)
        result = db.polls.update_one(
            {'_id': poll["_id"]},
            {'$set': {'votes': votes}, '$addToSet': {'users': user}},
        )
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
    user = User.from_json(session['User'])
    poll = Poll(request.form['question'], request.form.getlist('option[]'), user.username)
    db.polls.insert_one({'user': user.username, 'question': poll.question, 'options': poll.options, 'votes': poll.votes, 'users': poll.users})
    return redirect(url_for('index'))


@app.route('/debug')
def debug():
    users = list(db.users.find({}, {"_id": 0}))
    return users

@app.route('/delete_all_polls')
def delete_all_polls():
    try:
        result = db.polls.delete_many({})
        return jsonify({'message': 'Deleted {} polls'.format(result.deleted_count)}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run()

def ping_db():
    try:
        client.server_info() 
        return jsonify({'status': 'success', 'message': 'Database connection successful'})
    except errors.ServerSelectionTimeoutError as e:
        return jsonify({'status': 'error', 'message': 'Failed to connect to the database'})


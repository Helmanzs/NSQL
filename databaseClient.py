from pymongo import MongoClient, errors
from flask import session, jsonify
from user import User
from poll import Poll


class Database:
    def __init__(self, url: str):
        self.client = MongoClient(url)
        self.db = MongoClient(url).get_database('NSQL')

    def getPolls(self):
        polls = []
        try:
            polls = list(self.db.polls.find({}))
        except:
            return []
        
        for poll in polls:
            if session['User']['username'] in poll['users']:
                poll['disabled'] = True
            elif session['User']['username'] == poll['user']:
                poll['own'] = True
            else:
                poll['disabled'] = False
                poll['own'] = False
        return polls
       
    
    def register(self, username: str, password: str, email: str):
        try:
            if not self.db.users.find_one({'username': username}):
                user = User(username, password, email)
                self.db.users.insert_one({'username': user.username, 'password': user.password, 'email': user.email})
                session['User'] = User.to_json(user)
                return 1
            return 0
        except: 
            return 0
    
    def login(self, username: str, password: str):
        try:
            user_data = self.db.users.find_one({'username': username})
            if user_data and User.check_password(user_data['password'], password):
                user = User(username, password, user_data['email'])
                session['User'] = User.to_json(user)
                return 1
            return 0
        except: 
            return 0
    
    def logout(self):
        session.clear()
    
    def vote(self, index: int, polls: list, option: int):
        user = session['User']['username']
        poll = polls[index]
        votes = poll['votes']
        if user != poll['user']:
            votes[option] += 1
            poll['users'].append(user)
            self.db.polls.update_one(
                {'_id': poll["_id"]},
                {'$set': {'votes': votes}, '$addToSet': {'users': user}},
            )
            return 1
        return 0
    
    def submit_poll(self, question: str, options: list): 
        user = User.from_json(session['User'])
        poll = Poll(question, options, user.username)
        try:
            self.db.polls.insert_one({'user': user.username, 'question': poll.question, 'options': poll.options, 'votes': poll.votes, 'users': poll.users})
            return 1
        except:
            return 0
        
    def ping_db(self):
        try:
            self.client.server_info() 
            return jsonify({'status': 'success', 'message': 'Database connection successful'})
        except errors.ServerSelectionTimeoutError as e:
            return jsonify({'status': 'error', 'message': 'Failed to connect to the database'})

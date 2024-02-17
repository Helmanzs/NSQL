import redis
from pymongo import MongoClient, errors
from flask import session, jsonify
from user import User
from poll import Poll
import json
import time
from threading import Thread

class Database:
    def __init__(self, url: str):
        self.mongo_client = MongoClient(url)
        self.redis_client = redis.StrictRedis(host = 'redis',port = 6379, db = 0)
        self.db = self.mongo_client.get_database('NSQL')
        self.update_stable = False

        self.update_thread = Thread(target=self.periodic_mongo_update)
        self.update_thread.daemon = True
        self.update_thread.start()

    def periodic_mongo_update(self):
        while True:
            time.sleep(60)
            self.update_mongo_from_redis()

    def update_mongo_from_redis(self):
        polls = self.getPolls()

        for poll in polls:
            self.db.polls.update_one(
                {'_id': poll["_id"]},
                {'$set': {'votes': poll['votes'], 'users': poll['users']}}
            )
        print('Updating')

    def getPolls(self):
        polls = []

        try:
            if self.update_stable:
                polls = list(self.db.polls.find({}))
                self.update_stable = False
                for p in polls:
                        p['_id'] = str(p['_id'])
                self.redis_client.set('polls', json.dumps(polls))
            else:
                cached_polls = self.redis_client.get('polls')
                if cached_polls:
                    polls = json.loads(cached_polls)
                else:
                    polls = list(self.db.polls.find({}))
                    for p in polls:
                        p['_id'] = str(p['_id'])

                    self.redis_client.set('polls', json.dumps(polls))
        except Exception as e:
            print("Error retrieving polls:", e)
            raise
        return polls

    def register(self, username: str, password: str, email: str):
        try:
            if not self.db.users.find_one({'username': username}):
                user = User(username, password, email)
                self.db.users.insert_one({'username': user.username, 'password': user.password, 'email': user.email})
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
        except Exception as e: 
            print('error: ' + str(e))
            return 0
    
    def logout(self):
        session.clear()
    
    def vote(self, index: int, option: int):
        user = session['User']['username']
        polls = self.getPolls()
        poll = polls[index]

        votes = poll['votes']
        votes[option] += 1
        poll['users'].append(user)

        for p in polls:
            p['_id'] = str(p['_id'])

        self.redis_client.set('polls', json.dumps(polls))

    
    def submit_poll(self, question: str, options: list, user: str = ''): 
        if user == '':
            user = User.from_json(session['User']['username'])
        
        poll = Poll(question, options, user)
        try:
            self.db.polls.insert_one({'user': user, 'question': poll.question, 'options': poll.options, 'votes': poll.votes, 'users': poll.users})
            self.update_stable = True
            return 1
        except:
            return 0
        
    def ping_db(self):
        try:
            self.client.server_info() 
            return jsonify({'status': 'success', 'message': 'Database connection successful'})
        except errors.ServerSelectionTimeoutError as e:
            return jsonify({'status': 'error', 'message': 'Failed to connect to the database'})
        
    def delete_all(self):
        try:
            self.redis_client.flushdb()
            self.mongo_client.drop_database('NSQL')
            return jsonify({'status': 'ok'})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    def get_users(self):
        users_collection = self.db.get_collection('users')
        users = users_collection.find()
        return users

    def get_polls(self):
        polls_collection = self.db.get_collection('polls')
        polls = polls_collection.find()
        return polls

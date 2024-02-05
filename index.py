from flask import Flask, jsonify
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, Flask with MongoDB!'

uri = "mongodb+srv://nsql:nsql@cluster0.hopgxl2.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["sample_analytics"]

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

@app.route('/users')
def get_users():
    customers = db.customers
    users = list(customers.find())
    for user in users:
        if 'tier_and_details' in user:
            user['tier_and_details'] = str(user['tier_and_details'])

    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)
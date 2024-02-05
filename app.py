from flask import Flask, render_template
from mongo import db  # Import MongoDB connection

app = Flask(__name__)

@app.route('/')
def index():
    return "Flask app"

@app.route('/users')
def users():
    users_data = list(db.users.find({}, {'_id': 0}))
    return render_template('db_template.html', users=users_data)

if __name__ == '__main__':
    app.run(debug=True)


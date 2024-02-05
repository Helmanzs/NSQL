from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/mongo/")
def hello_mongo():
    return "<p>Hello, Mongo!</p>"
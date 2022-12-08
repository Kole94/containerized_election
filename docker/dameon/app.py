from flask import Flask, render_template, request,redirect, url_for,session, make_response,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
import pymysql 
import os
import redis
import threading 

listen = ['default']
app = Flask(__name__)
socket_location = "/var/run/mysqld/mysqld.sock"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:password@172.17.0.1:33063/db?unix_socket=".format(
    'localhost'
)
db = SQLAlchemy()
db.init_app(app)
r  = redis.Redis(host="redis", port="6379", db=0)

class Votes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username):
        self.username = username

with app.app_context():
    print("Dsadasdadasdas")
    db.create_all()

@app.route('/')
def handleVote():
    while True:
        name = r.lpop('vote')
        if name:
            try:
                vote = Votes(name)
                with app.app_context():

                    db.session.add(vote)
                    db.session.commit()
                    return jsonify(votes)
            except ValueError as e:
                    return e 

thread = threading.Thread(target=handleVote())

thread.start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) 

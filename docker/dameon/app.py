from flask import Flask, render_template, request,redirect, url_for,session, make_response,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token,get_jwt_identity,get_jwt;
import pymysql 
import os
import time
import redis
from rq import Worker, Queue, Connection
import threading 
# import _thead
listen = ['default']
app = Flask(__name__)
socket_location = "/var/run/mysqld/mysqld.sock"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:password@172.17.0.1:33063/db?unix_socket=".format(
    'localhost'
)
db = SQLAlchemy()
db.init_app(app)
r  = redis.Redis(host="redis", port="6379", db=0)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

    def __init__(self, username):
        self.username = username

    # def __repr__(self):
    #     return '<User %r>' % self.username
with app.app_context():
    db.create_all()


# def hello_geek():
#     return r.lpop('foo')

    # vote = Vote(username='velebit')
    # db.session.add(vote)
    # db.session.commit()
    # r.delete('velebit')
#     b = r.lpop('foo')
#     return b
@app.route('/')
def thread_function():
    a = r.lpop('foo')
    return a
    # while True:
    #     print('das')
        # a = r.lpop('foo')
        # if a:
        #     print(a)
            # print(r.lpop('foo'))
#     m = r.get('velebit')
#     if m: 
#         hello_geek()
#         r.delete('velebit')  
# thread_function('dsa')
# while True:
#     vote = r.lpop('vote')
#     if(vote):
#         print(vote)
threading.Thread(target=thread_function, args=(), daemon=True).start()

if __name__ == "__main__":
    # threading.Thread(target=thread_function, args=(), daemon=True).start()
    # x.start()
    app.run(host="0.0.0.0", debug=True)

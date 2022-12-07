from flask import Flask, render_template, request,redirect, url_for,session, make_response,jsonify,Response
# from flask_sqlalchemy import SQLAlchemy
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token,get_jwt_identity,get_jwt;
# import pymysql 
# from datetime import timedelta;
import os

import redis
from rq import Worker, Queue, Connection

listen = ['default']
app = Flask(__name__)

# redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')

# conn = redis.from_url(redis_url)


r  = redis.Redis(host="redis", port="6379")
# queue = Queue(connection=r)
# if __name__ == '__main__':
#     with Connection(conn):
#         worker = Worker(list(map(Queue, listen)))
#         worker.work()


@app.route('/', methods=["GET"])
def hello_geek():
    r.set('velebit',1)

    return '<h1>Hello from Flask & Docker</h2>'

@app.route('/get')
def get_geek():
    # job = queue.enqueu*
    # m = r.get('velebit')
    r.rpush('foo', *[1,2,3,4])

    # r.delete('velebit')
    return 'm'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) 

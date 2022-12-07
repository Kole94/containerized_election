from flask import Flask, render_template, request,redirect, url_for,session, make_response,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token,get_jwt_identity,get_jwt;
import pymysql 
from datetime import timedelta;

app = Flask(__name__)
socket_location = "/var/run/mysqld/mysqld.sock"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:password@172.17.0.1:33063/db?unix_socket=".format(
    'localhost'
)

db = SQLAlchemy()
db.init_app(app)
app.config["JWT_SECRET_KEY"] = "super-secret" 
jwtM = JWTManager(app)

class ElectionParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    # individual = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name
        # self.individual = individual
        # self.id = id
with app.app_context():
    db.create_all()

class Election(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.String(256))
    end = db.Column(db.String(256))
    # individual = db.Column(Boolean)
    # participants = db.ARRAY(Integer)

    def __init__(self, start, end):
        self.start = start
        self.end = end
        # self.individual = individual
        # self.participants = participants

@app.route("/createParticipan",methods=["POST"])
@jwt_required()
def createParticipan():
    request_data = request.get_json()
    name = request_data["name"]
    # individual = request_data["individual"]
    try:
        participant = ElectionParticipant(name=name)
        db.session.add(participant)
        db.session.commit()
        return jsonify(name)
    except ValueError as e:
            return e


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) 

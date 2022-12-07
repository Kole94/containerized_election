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
# app.config["SQLALCHEMY_BINDS"] = {
    # 'users':  "mysql+pymysql://user:password@172.17.0.1:3350/db?unix_socket=".format('localhost')
# }

db = SQLAlchemy()
db.init_app(app)
app.config["JWT_SECRET_KEY"] = "super-secret" 
jwtM = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    jmbg = db.Column(db.String(120), unique=True)
    name = db.Column(db.String(120), unique=True)
    lastname = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)

    def __init__(self, username, email,jmbg,name,lastname,password):
        self.username = username
        self.email = email
        self.jmbg = jmbg
        self.password = password
        self.name = name
        self.lastname = lastname

    def __repr__(self):
        return '<User %r>' % self.username
    
    def getPassword(self):
        return self.password

with app.app_context():
    db.create_all()

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'


@app.route("/register",methods=["POST","GET"])
def register():
    if request.method == "POST":
        try:
            request_data = request.get_json()

            username = request_data["username"]
            email = request_data["email"]
            jmbg = request_data["jmbg"]
            password = request_data["password"]
            name = request_data["name"]
            lastname = request_data["lastname"]  
            user = User(username,email,jmbg,name,lastname,password)
            db.session.add(user)
            db.session.commit()
            return "ok"
        except ValueError as e:
            return render_template('error.html',statusCode=400, message=e)
    if request.method == "GET":
        return render_template("register.html")


@app.route("/login",methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return "login.html"

    else:
        try:
            request_data = request.get_json()
            email = request_data["email"]
            password = request_data["password"]
            user = User.query.filter_by(email=email).first()
            if(user.getPassword() == password):
                accessToken = create_access_token(identity=email, additional_claims={"user":"abc"},expires_delta=timedelta(minutes=30)) 
                refreshToken = create_refresh_token(identity=email,  additional_claims={"user":"abc"})            
                return jsonify(token= accessToken, refresh=refreshToken)
        except ValueError as e:
            return render_template('error.html',statusCode=400, message=e)


@app.route("/user",methods=["GET"])
@jwt_required()
def user():
    try:
        return f"<div><h1>ok</h1></div>"
    except ValueError as e:
        return render_template('error.html',statusCode=400, message=e)


@app.route("/refresh",methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity=get_jwt_identity()
    refreshClaims=get_jwt()
    return Response (create_access_token(identity=identity,  additional_claims={"user":"abc"}), status=200)         


@app.route("/delete",methods=["POST"])
def delete():
    request_data = request.get_json()
    email = request_data["email"]
    user = User.query.filter_by(email=email).first()
    if user is None:
        abort(404)
    db.session.delete(user)
    db.session.commit()

    return "deleted"


class ElectionParticipant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    # individual = db.Column(db.String(120), unique=True)

    def __init__(self, name, individual):
        self.name = name
        # self.individual = individual
        # self.id = id

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

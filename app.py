from flask import Flask, render_template, request,redirect, url_for,session, make_response,jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, create_refresh_token,get_jwt_identity,get_jwt;
import pymysql 
from datetime import timedelta;

app = Flask(__name__)
socket_location = "/var/run/mysqld/mysqld.sock"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://user:password@172.17.0.1:3306/db?unix_socket=".format(
    'localhost'
)
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True) 
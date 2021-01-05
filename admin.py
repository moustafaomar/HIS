from flask import Flask, jsonify,request,make_response
import mysql.connector
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = "ADMINSECRETKEY"

#SQL Connection 
def SQL_CONN():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="databaseproject"
    )
    conn = mydb.cursor(buffered=True)
    return [conn,mydb]

#Middleware for admin
def admin_middleware(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'token is missing'}),401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            if data['role'] != 'admin':
                return jsonify({'message':'incorrect user role'}),401
        except:
            return jsonify({'message': 'Token is invalid'}),401
        return f(*args,**kwargs)
    return decorated

#Create a new admin
def create_admin():
    [conn,mydb] = SQL_CONN()
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'],method='sha256')
    query = "INSERT INTO admin(username,password) VALUES(%s,%s)"
    values = (data['username'],hashed_password)
    conn.execute(query,values)
    mydb.commit()
    return jsonify({'message': "Created"})
#admin Login
def admin_login():
    [conn,mydb] = SQL_CONN()
    data = request.get_json()
    query="SELECT password,id FROM admin WHERE username = %s"
    values=(data['username'],)
    conn.execute(query,values)
    result=conn.fetchone()
    if(result):
        if check_password_hash(result[0],data['password']):
            token = jwt.encode({'user':result[1],'role':'admin','exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
            return jsonify({'token':token.decode('utf-8')})
        else:
            return jsonify({
                'message': "Incorrect Password",
            })
    else:
        return jsonify({'message':"username doesn't exist"})
@admin_middleware
def admin_protected_area():
    return jsonify({'message':'Entered'})
@admin_middleware
def get_data():
    token = request.headers['x-access-token']
    [conn,mydb] = SQL_CONN()
    query = "SELECT username FROM admin WHERE id = %s"
    values = (jwt.decode(token,app.config['SECRET_KEY'])['user'],)
    conn.execute(query,values)
    return jsonify({'message':conn.fetchone()})
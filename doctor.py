from flask import Flask, jsonify,request,make_response
import mysql.connector
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
app = Flask(__name__)
app.config['SECRET_KEY'] = "DOCTORSECRETKEY"

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

#Middleware for doctor
def doctor_middleware(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'token is missing'}),401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            if data['role'] != 'doctor':
                return jsonify({'message':'incorrect user role'}),401
        except:
            return jsonify({'message': 'Token is invalid'}),401
        return f(*args,**kwargs)
    return decorated

#Create a new doctor
def create_doctor():
    [conn,mydb] = SQL_CONN()
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'],method='sha256')
    query = "INSERT INTO doctor(SSN,Name,email,phone,start_hour,end_hour,password) VALUES(%s,%s,%s,%s,%s,%s,%s)"
    values = (data['SSN'],data['Name'],data['email'],data['phone'],data['start_hour'],data['end_hour'],hashed_password)
    conn.execute(query,values)
    mydb.commit()
    return jsonify({'message': "Created"})
#Doctor Login
def doctor_login():
    [conn,mydb] = SQL_CONN()
    data = request.get_json()
    query="SELECT password FROM doctor WHERE SSN=%s"
    values=(data['SSN'],)
    conn.execute(query,values)
    result=conn.fetchone()
    if(result):
        if check_password_hash(result[0],data['password']):
            token = jwt.encode({'user':data['SSN'],'role':'doctor','exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=120)},app.config['SECRET_KEY'])
            return jsonify({'token':token.decode('UTF-8')})
        else:
            return jsonify({
                'message': "Incorrect Password",
            })
    else:
        return jsonify({'message':"SSN doesn't exist"})
@doctor_middleware
def doctor_protected_area():
    return jsonify({'message':'Entered'})
@doctor_middleware
def get_data():
    token = request.headers['x-access-token']
    [conn,mydb] = SQL_CONN()
    query = "SELECT Name FROM doctor WHERE SSN = %s"
    values = (jwt.decode(token,app.config['SECRET_KEY'])['user'],)
    conn.execute(query,values)
    return jsonify({'message':conn.fetchone()})
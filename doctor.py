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
            return jsonify({'token':token.decode('utf-8')})
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
    query = "SELECT Name,start_hour,end_hour FROM doctor WHERE SSN = %s"
    values = (jwt.decode(token,app.config['SECRET_KEY'])['user'],)
    conn.execute(query,values)
    result = conn.fetchone()
    today = datetime.datetime.today()
    delta1 = str(result[1])
    delta1 = delta1.split(':')
    delta2 = str(result[2])
    delta2 = delta2.split(':')
    starttime = today.replace(hour=int(delta1[0]),minute=int(delta1[1]),second=int(delta1[2]),microsecond=0).isoformat()
    endtime = today.replace(hour=int(delta2[0]),minute=int(delta2[1]),second=int(delta2[2]),microsecond=0).isoformat()
    query = "SELECT COUNT(PSSN) FROM doctor JOIN patient_doctor ON DSSN=doctor.SSN WHERE SSN = %s GROUP BY SSN"
    values = (jwt.decode(token,app.config['SECRET_KEY'])['user'],)
    conn.execute(query,values)
    resultc = conn.fetchone()
    if not resultc:
        resultc = (0,)
    query = "SELECT Name,SSN FROM patient join patient_doctor ON PSSN=patient.SSN WHERE DSSN=%s"
    values = (jwt.decode(token,app.config['SECRET_KEY'])['user'],)
    conn.execute(query,values)
    result2 = [conn.fetchall()]
    result = (result[0],starttime,endtime)+resultc+tuple(result2)
    return jsonify({'message':result})
@doctor_middleware
def get_files(pid):
    token = request.headers['x-access-token']
    [conn,mydb] = SQL_CONN()
    query = "SELECT FileURL,Filename FROM patient_files JOIN patient ON PSSN=patient.SSN WHERE DSSN = %s AND patient.SSN = %s"
    values = (jwt.decode(token,app.config['SECRET_KEY'])['user'],pid)
    conn.execute(query,values)
    result = tuple([conn.fetchall()])
    return jsonify({'message':result})
@doctor_middleware
def get_rooms():
    token = request.headers['x-access-token']
    [conn,mydb] = SQL_CONN()
    data = request.get_json()
    query="SELECT roomno FROM icu WHERE doctor_ssn=%s"
    values=(jwt.decode(token,app.config['SECRET_KEY'])['user'],)
    conn.execute(query,values)
    result=conn.fetchall()
    return jsonify({'data':result})
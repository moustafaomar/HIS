from flask import Flask, jsonify,request,make_response
import mysql.connector
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
import doctor
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
@admin_middleware
def link_users():
    data = request.get_json()
    [conn,mydb] = SQL_CONN()
    query = "INSERT INTO patient_doctor(DSSN,PSSN) VALUES (%s,%s)"
    values = (data['did'],data['pid'])
    conn.execute(query,values)
    mydb.commit()
    return jsonify({'message': 'Relation Created'})
@admin_middleware
def get_related_users():
    [conn,mydb] = SQL_CONN()
    query = "SELECT patient.Name,doctor.Name FROM patient JOIN patient_doctor ON patient.SSN = PSSN JOIN doctor ON doctor.SSN = DSSN"
    conn.execute(query)
    result = conn.fetchall()
    return jsonify({'message': 'Relation Created', 'data':result})
# patients on admin area
@admin_middleware
def get_patients():
    [conn,mydb] = SQL_CONN()
    query = "SELECT patient.Name,patient.SSN,patient.phone FROM patient"
    conn.execute(query)
    result = conn.fetchall()
    return jsonify({'message': 'Fetched', 'data':result})
@admin_middleware
def delete_patients():
    data = request.get_json()
    [conn,mydb] = SQL_CONN()
    query = "DELETE FROM patient WHERE SSN = %s"
    values = (data['ssn'],)
    conn.execute(query,values)
    mydb.commit()
    return jsonify({'message': 'Deleted'})
@admin_middleware
def get_edit_patient(ssn):
    data = request.get_json()
    [conn,mydb] = SQL_CONN()
    query = "SELECT Name,phone FROM patient WHERE SSN = %s"
    values = (ssn,)
    conn.execute(query,values)
    result = conn.fetchone()
    return jsonify({'message': 'fetched','data':result})
@admin_middleware
def edit_patient():
    data = request.get_json()
    [conn,mydb] = SQL_CONN()
    query = "UPDATE patient SET Name=%s, phone=%s WHERE SSN = %s"
    values = (data['Name'],data['phone'],data['SSN'])
    conn.execute(query,values)
    mydb.commit()
    return jsonify({'message': 'updated'})
# doctors on admin area
@admin_middleware
def get_doctors():
    [conn,mydb] = SQL_CONN()
    query = "SELECT doctor.Name,doctor.SSN,doctor.email,doctor.phone FROM doctor"
    conn.execute(query)
    result = conn.fetchall()
    return jsonify({'message': 'Fetched', 'data':result})
@admin_middleware
def delete_doctors():
    data = request.get_json()
    [conn,mydb] = SQL_CONN()
    query = "DELETE FROM doctor WHERE SSN = %s"
    values = (data['ssn'],)
    conn.execute(query,values)
    mydb.commit()
    return jsonify({'message': 'Deleted'})
@admin_middleware
def get_edit_doctor(ssn):
    data = request.get_json()
    [conn,mydb] = SQL_CONN()
    query = "SELECT Name,phone,email FROM doctor WHERE SSN = %s"
    values = (ssn,)
    conn.execute(query,values)
    result = conn.fetchone()
    return jsonify({'message': 'fetched','data':result})
@admin_middleware
def edit_doctor():
    data = request.get_json()
    [conn,mydb] = SQL_CONN()
    query = "UPDATE doctor SET Name=%s, phone=%s, email=%s WHERE SSN = %s"
    values = (data['Name'],data['phone'],data['email'],data['SSN'])
    conn.execute(query,values)
    mydb.commit()
    return jsonify({'message': 'updated'})
@admin_middleware
def create_doctor():
    return doctor.create_doctor()
@admin_middleware
def get_stats():
    [conn,mydb] = SQL_CONN()
    query = "SELECT COUNT(SSN) FROM patient"
    conn.execute(query)
    result = conn.fetchone()
    if not result:
        result = (0,)
    query = "SELECT COUNT(SSN) FROM doctor"
    conn.execute(query)
    result2 = conn.fetchone()
    if not result2:
        result2 = (0,)
    final = result+result2
    return jsonify({"message":final})
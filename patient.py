from flask import Flask, jsonify,request,make_response
import mysql.connector
import os
import jwt
import datetime
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['SECRET_KEY'] = "PATIENTSECRETKEY"
UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#Allow only specific filetypes to be uploaded
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file():
    if 'file' not in request.files:
        return False
        file = request.files['file']
        if file.filename == '':
            return False
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return filename

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

#Middleware for patient
def patient_middleware(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message':'token is missing'}),401
        try:
            data = jwt.decode(token,app.config['SECRET_KEY'])
            if data['role'] != 'patient':
                return jsonify({'message':'incorrect user role'}),401
        except:
            return jsonify({'message': 'Token is invalid'}),401
        return f(*args,**kwargs)
    return decorated

#Create a new patient
def create_patient():
    [conn,mydb] = SQL_CONN()
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'],method='sha256')
    query = "INSERT INTO patient(SSN,Name,phone,password) VALUES(%s,%s,%s,%s)"
    values = (data['SSN'],data['Name'],data['phone'],hashed_password)
    conn.execute(query,values)
    mydb.commit()
    return jsonify({'message': "Created"})
#Patient Login
def patient_login():
    [conn,mydb] = SQL_CONN()
    data = request.get_json()
    query="SELECT password FROM patient WHERE SSN=%s"
    values=(data['SSN'],)
    conn.execute(query,values)
    result=conn.fetchone()
    if(result):
        if check_password_hash(result[0],data['password']):
            token = jwt.encode({'user':data['SSN'],'role':'patient','exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},app.config['SECRET_KEY'])
            return jsonify({'token':token.decode('UTF-8')})
        else:
            return jsonify({
                'message': "Incorrect Password",
            })
    else:
        return jsonify({'message':"SSN doesn't exist"})
@patient_middleware
def patient_protected_area():
    return jsonify({'message':'Entered'})
@patient_middleware
def patient_upload_file(pid,did):
    file = upload_file()
    if file:
        [conn,mydb] = SQL_CONN()
        query = "INSERT INTO patient_files(PSSN,Filename,FileURL,DSSN) VALUES(%s,%s,%s,%s)"
        values = (pid,file,"http://localhost:5000/upload/"+file,did)
        conn.execute(query,values)
        mydb.commit()

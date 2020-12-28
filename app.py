from flask import Flask, jsonify,request,make_response
import mysql.connector
import jwt
import datetime
import doctor
import patient
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
#create doctor route
app.add_url_rule('/doctor/register','create_doctor',view_func=doctor.create_doctor,methods=['POST'])
#create patient route
app.add_url_rule('/patient/register','create_patient',view_func=patient.create_patient,methods=['POST'])
#doctor login route
app.add_url_rule('/doctor/login','login_doctor',view_func=doctor.doctor_login,methods=['POST'])
#patient login route
app.add_url_rule('/patient/login','login_patient',view_func=patient.patient_login,methods=['POST'])
#Doctor protected route
app.add_url_rule('/doctor/dashboard','protected_doctor',view_func=doctor.doctor_protected_area,methods=['GET'])
#Patient protected route
app.add_url_rule('/patient/dashboard','protected_patient',view_func=patient.patient_protected_area,methods=['GET'])

#Patient file upload route
app.add_url_rule('/patient/<int:pid>/<int:did>','upload_patient',view_func=patient.patient_upload_file,methods=['POST'])

#Patient data getter route
app.add_url_rule('/patient/getdata','data_patient',view_func=patient.get_data,methods=['POST'])


if __name__ == '__main__':
   app.run()
from flask import Flask, jsonify,request,make_response
import mysql.connector
import jwt
import datetime
import doctor
import patient
import admin
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
#create doctor route
app.add_url_rule('/doctor/register','create_doctor',view_func=doctor.create_doctor,methods=['POST'])
#create patient route
app.add_url_rule('/patient/register','create_patient',view_func=patient.create_patient,methods=['POST'])
#create admin route
app.add_url_rule('/admin/register','create_admin',view_func=admin.create_admin,methods=['POST'])
#doctor login route
app.add_url_rule('/doctor/login','login_doctor',view_func=doctor.doctor_login,methods=['POST'])
#patient login route
app.add_url_rule('/patient/login','login_patient',view_func=patient.patient_login,methods=['POST'])
#admin login route
app.add_url_rule('/admin/login','login_admin',view_func=admin.admin_login,methods=['POST'])
#Doctor protected route
app.add_url_rule('/doctor/dashboard','protected_doctor',view_func=doctor.doctor_protected_area,methods=['GET'])
#Patient protected route
app.add_url_rule('/patient/dashboard','protected_patient',view_func=patient.patient_protected_area,methods=['GET'])
#admin protected route
app.add_url_rule('/admin/dashboard','protected_admin',view_func=admin.admin_protected_area,methods=['GET'])
#Patient file upload route
app.add_url_rule('/patient/<int:pid>/<int:did>','upload_patient',view_func=patient.patient_upload_file,methods=['POST'])

#Patient data getter route
app.add_url_rule('/patient/getdata','data_patient',view_func=patient.get_data,methods=['POST'])

#Doctor data getter route
app.add_url_rule('/doctor/getdata','data_doctor',view_func=doctor.get_data,methods=['POST'])

#Admin data getter route
app.add_url_rule('/admin/getdata','data_admin',view_func=admin.get_data,methods=['POST'])


if __name__ == '__main__':
   app.run()
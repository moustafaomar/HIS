from flask import Flask, jsonify,request,make_response,send_from_directory
import mysql.connector
import jwt
import datetime
import doctor
import patient
import admin
from mailjet_rest import Client
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
#create doctor route
app.add_url_rule('/admin/doctor/create','create_doctor',view_func=admin.create_doctor,methods=['POST'])
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

#Doctor data getter route
app.add_url_rule('/doctor/getfiles/<int:pid>','data_files_doctor',view_func=doctor.get_files,methods=['POST'])


#Admin data getter route
app.add_url_rule('/admin/getdata','data_admin',view_func=admin.get_data,methods=['POST'])

#Admin data getter route
app.add_url_rule('/admin/getstats','stats_admin',view_func=admin.get_stats,methods=['POST'])

#Admin link users route
app.add_url_rule('/admin/relate','relate_admin',view_func=admin.link_users,methods=['POST'])

#Admin get linked users route
app.add_url_rule('/admin/get_related','get_related_admin',view_func=admin.get_related_users,methods=['GET'])

@app.route('/uploads/<path:filename>')
def files(filename):
  return send_from_directory('uploads/', filename)
@app.route('/formsubmit',methods=['POST'])
def formsubmit():
   data = request.get_json()
   mailjet = Client(auth=('ce59a2d52188c2a87f4a1f1deb067ed9', '60342a20254bd7c13a937c29791cfad7'), version='v3.1')
   data = {
   'Messages': [
               {
                     "From": {
                           "Email": data['email'],
                           "Name": data['name']
                     },
                     "To": [
                           {
                                 "Email": "moustafaomar200@gmail.com",
                                 "Name": "Mostafa"
                           }
                     ],
                     "Subject": "Mail from HIS",
                     "TextPart": data['content'],
               }
         ]
   }
   result = mailjet.send.create(data=data)
   return result.json()
if __name__ == '__main__':
   app.run()
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
#Get patients route
app.add_url_rule('/admin/patients','fetch_patients',view_func=admin.get_patients,methods=['GET'])
#Get doctors route
app.add_url_rule('/admin/doctors','fetch_doctors',view_func=admin.get_doctors,methods=['GET'])

#Delete patients route
app.add_url_rule('/admin/deleteP','delete_patients',view_func=admin.delete_patients,methods=['POST'])

#Delete doctors route
app.add_url_rule('/admin/deleteD','delete_doctors',view_func=admin.delete_doctors,methods=['POST'])

#Add doctors to room route
app.add_url_rule('/admin/DtR','room_doctors',view_func=admin.add_to_room,methods=['POST'])

#Get available rooms Doc
app.add_url_rule('/admin/DtR/get','room_doctors_getter',view_func=admin.get_rooms,methods=['GET'])

#Add patients to room route
app.add_url_rule('/admin/PtR','room_patients',view_func=admin.add_to_room_p,methods=['POST'])

#Get available rooms Doc
app.add_url_rule('/admin/PtR/get','room_patients_getter',view_func=admin.get_rooms_p,methods=['GET'])

#Get rooms in use
app.add_url_rule('/admin/get_rooms','room_get',view_func=admin.get_free_rooms,methods=['GET'])

#Clear rooms in use
app.add_url_rule('/admin/clear_room','clear_room',view_func=admin.clear_room,methods=['POST'])

#Clear pat_doc relation
app.add_url_rule('/admin/unrelate','unrelate',view_func=admin.unrelate,methods=['POST'])


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
app.add_url_rule('/doctor/rooms','doctors_rooms',view_func=doctor.get_rooms,methods=['GET'])


#Doctor data getter route
app.add_url_rule('/doctor/getfiles/<int:pid>','data_files_doctor',view_func=doctor.get_files,methods=['POST'])

#Patient data getter for edit route
app.add_url_rule('/admin/patient/get/<int:ssn>','data_edit_patient',view_func=admin.get_edit_patient,methods=['GET'])

#Patient updater route
app.add_url_rule('/admin/patient/edit','edit_patient',view_func=admin.edit_patient,methods=['POST'])

#Doctor data getter for edit route
app.add_url_rule('/admin/doctor/get/<int:ssn>','data_edit_doctor',view_func=admin.get_edit_doctor,methods=['GET'])

#Doctor updater route
app.add_url_rule('/admin/doctor/edit','edit_doctor',view_func=admin.edit_doctor,methods=['POST'])




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
                           "Email": "moustafaomar200@gmail.com",
                           "Name": data['name']
                     },
                     "To": [
                           {
                                 "Email": "moustafaomar200@gmail.com",
                                 "Name": "Mostafa"
                           }
                     ],
                     "Subject": "Mail from HIS",
                     "TextPart": "Email: "+data['email']+"\n"+"Content: "+data['content'],
               }
         ]
   }
   result = mailjet.send.create(data=data)
   return result.json()
if __name__ == '__main__':
   app.run()
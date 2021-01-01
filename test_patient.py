import patient
import unittest
from flask.testing import FlaskClient
from app import app
from flask import jsonify
import json
class TestPatientMethods(unittest.TestCase):
    def test_conn(self):
        self.assertTrue(patient.SQL_CONN())
    def test_create_patient(self):
        tester = app
        with tester.test_request_context(
        '/patient/signup', json={'SSN': '10500', 'Name' : 'TestPatient', 'phone' : '010101010', 'password' : 'test_password'}):
            self.assertTrue(patient.create_patient())
    #true test for login
    def test_patient_login(self):
        tester = app
        with tester.test_request_context(
        '/patient/login', json={'SSN': '10500', 'password' : 'test_password'}):
            expected = 'token'
            response = patient.patient_login()
            response = response.response[0].decode('utf-8')
            self.assertIn(expected,response)
    #incorrect login, SSN doesn't exist
    def test_patient_data_with_ssn_that_doesnt_exist(self):
        tester = app
        with tester.test_request_context(
        '/patient/login', json={'SSN': '0', 'password' : 'test_password'}):
            expected = '{"message":"SSN doesn\'t exist"}\n'
            response = patient.patient_login()
            response = response.response[0].decode('utf-8')
            self.assertEqual(response,expected)
    #incorrect login
    def test_patient_data_with_incorrect_password(self):
        tester = app
        with tester.test_request_context(
        '/patient/login', json={'SSN': '10500', 'password' : 'atest_password'}):
            expected = '{"message":"Incorrect Password"}\n'
            response = patient.patient_login()
            response = response.response[0].decode('utf-8')
            self.assertEqual(response,expected)
            
    def test_patient_data_without_token(self):
        tester = app
        with tester.test_request_context(
        '/patient/dashboard', headers={'x-access-token': ''}):
            response = patient.get_data()[0]
            response = response.response[0].decode('utf-8')
            expected = '{"message":"token is missing"}\n'
            self.assertEqual(response,expected)
    def test_patient_data_with_token(self):
        tester = app
        with tester.test_request_context(
        '/patient/dashboard', headers={'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMTA1MDAiLCJyb2xlIjoicGF0aWVudCIsImV4cCI6MzA3NjgwMDAwMH0.xFQSEuuNVJKA0U3ZRw-r6YDtl-bNduIwewu3RTztTtw'}):
            response = patient.get_data()
            #response = response.response[0].decode('utf-8')
            response = response.text.decode('utf-8')
            expected = '{"message":["TestPatient"]}\n'
            self.assertEqual(response,expected)
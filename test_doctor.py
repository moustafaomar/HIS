import doctor
import unittest
from flask.testing import FlaskClient
from app import app
from flask import jsonify
import json
class TestDoctorMethods(unittest.TestCase):
    def test_conn(self):
        self.assertTrue(doctor.SQL_CONN())
    def test_create_doctor(self):
        tester = app
        with tester.test_request_context(
        '/doctor/create', json={'SSN': '10500', 'Name' : 'TestUser', 'email' : 'info@test.com', 'phone' : '010101010', 'start_hour' : '00:00', 'end_hour' : '00:00', 'password' : 'test_password'}):
            self.assertTrue(doctor.create_doctor())
    #true test for login
    def test_doctor_login(self):
        tester = app
        with tester.test_request_context(
        '/doctor/login', json={'SSN': '10500', 'password' : 'test_password'}):
            expected = 'token'
            response = doctor.doctor_login()
            response = response.response[0].decode('utf-8')
            self.assertIn(expected,response)
    #incorrect login, SSN doesn't exist
    def test_doctor_data_with_ssn_that_doesnt_exist(self):
        tester = app
        with tester.test_request_context(
        '/doctor/login', json={'SSN': '0', 'password' : 'test_password'}):
            expected = '{"message":"SSN doesn\'t exist"}\n'
            response = doctor.doctor_login()
            response = response.response[0].decode('utf-8')
            self.assertEqual(response,expected)
    #incorrect login
    def test_doctor_data_with_incorrect_password(self):
        tester = app
        with tester.test_request_context(
        '/doctor/login', json={'SSN': '10500', 'password' : 'atest_password'}):
            expected = '{"message":"Incorrect Password"}\n'
            response = doctor.doctor_login()
            response = response.response[0].decode('utf-8')
            self.assertEqual(response,expected)
            
    def test_doctor_data_without_token(self):
        tester = app
        with tester.test_request_context(
        '/doctor/dashboard', headers={'x-access-token': ''}):
            response = doctor.get_data()[0]
            response = response.response[0].decode('utf-8')
            expected = '{"message":"token is missing"}\n'
            self.assertEqual(response,expected)
    def test_doctor_data_with_token(self):
        tester = app
        with tester.test_request_context(
        '/doctor/dashboard', headers={'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMTA1MDAiLCJyb2xlIjoiZG9jdG9yIiwiZXhwIjozMDc2ODAwMDAwfQ.uJw1T4sNhSAN0U5eb4X61gtwaXr3e1h7AtAan-bHnGQ'}):
            response = doctor.get_data()
            response = response.response[0].decode('utf-8')
            expected = '{"message":["TestUser"]}\n'
            self.assertEqual(response,expected)
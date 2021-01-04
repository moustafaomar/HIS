import admin
import unittest
from flask.testing import FlaskClient
from app import app
from flask import jsonify
import json
class TestAdminMethods(unittest.TestCase):
    def test_conn(self):
        self.assertTrue(admin.SQL_CONN())
    def test_create_admin(self):
        tester = app
        with tester.test_request_context(
        '/admin/signup', json={'username': 'admin', 'password' : 'test_password'}):
            self.assertTrue(admin.create_admin())
    #true test for login
    def test_admin_login(self):
        tester = app
        with tester.test_request_context(
        '/admin/login', json={'username': 'admin', 'password' : 'test_password'}):
            expected = 'token'
            response = admin.admin_login()
            response = response.response[0].decode('utf-8')
            self.assertIn(expected,response)
    #incorrect login, username doesn't exist
    def test_admin_data_with_username_that_doesnt_exist(self):
        tester = app
        with tester.test_request_context(
        '/admin/login', json={'username': '0', 'password' : 'test_password'}):
            expected = '{"message":"username doesn\'t exist"}\n'
            response = admin.admin_login()
            response = response.response[0].decode('utf-8')
            self.assertEqual(response,expected)
    #incorrect login
    def test_admin_data_with_incorrect_password(self):
        tester = app
        with tester.test_request_context(
        '/admin/login', json={'username': 'admin', 'password' : 'atest_password'}):
            expected = '{"message":"Incorrect Password"}\n'
            response = admin.admin_login()
            response = response.response[0].decode('utf-8')
            self.assertEqual(response,expected)
            
    def test_admin_data_without_token(self):
        tester = app
        with tester.test_request_context(
        '/admin/dashboard', headers={'x-access-token': ''}):
            response = admin.get_data()[0]
            response = response.response[0].decode('utf-8')
            expected = '{"message":"token is missing"}\n'
            self.assertEqual(response,expected)
    def test_admin_data_with_token(self):
        tester = app
        with tester.test_request_context(
        '/admin/dashboard', headers={'x-access-token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjoiMSIsInJvbGUiOiJhZG1pbiIsImV4cCI6MzA3NjgwMDAwMH0.DMZ7mGKqHwuWCgILx9w7M0OAxrsx6B3DbpVl_w5oEAc'}):
            response = admin.get_data()
            response = response.response[0].decode('utf-8')
            expected = '{"message":["admin"]}\n'
            self.assertEqual(response,expected)
import admin
import unittest
from flask.testing import FlaskClient
from app import app
from flask import jsonify
import json
import datetime
import jwt
import mysql.connector
class TestAdminMethods(unittest.TestCase):
    def test_conn(self):
        self.assertTrue(admin.SQL_CONN())
    def test_create_admin(self):
        tester = app
        with tester.test_request_context(
        '/admin/register', json={'username': 'test', 'password' : 'test_password'}):
            self.assertTrue(admin.create_admin())
    #incorrect login, username doesn't exist
    def test_admin_data_with_username_that_doesnt_exist(self):
        tester = app
        with tester.test_request_context(
        '/admin/login', json={'username': '0', 'password' : 'test_password'}):
            expected = '{"message":"username doesn\'t exist"}\n'
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
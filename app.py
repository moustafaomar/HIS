from flask import Flask, jsonify
import mysql.connector
app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify(name="Mostafa",b=2)
if __name__ == '__main__':
   app.run()
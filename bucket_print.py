from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from boto3 import client, Session
import boto3

app = Flask(__name__)

prefix = '...'
ACCESS_KEY='AKIAIXA6OUMPEQ5MWAXQ'
SECRET_KEY='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'

session = Session(aws_access_key_id=ACCESS_KEY,
                  aws_secret_access_key=SECRET_KEY)
s3 = session.resource('s3')
your_bucket = s3.Bucket('podcastchannel')

s3_client = boto3.client('s3',
                         aws_access_key_id = ACCESS_KEY,
                         aws_secret_access_key = SECRET_KEY)

@app.route('/')
def index():
    return render_template('home.html')

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)

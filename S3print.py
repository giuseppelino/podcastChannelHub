from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from boto3 import client
import boto3

app = Flask(__name__)

AWS_ACCESS_KEY_ID = 'AKIAIXA6OUMPEQ5MWAXQ'
AWS_SECRET_ACCESS_KEY = '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'

s3_client = boto3.client('s3',
                         aws_access_key_id=AWS_ACCESS_KEY_ID,
                         aws_secret_access_key= AWS_SECRET_ACCESS_KEY)
bucket_name = 'podcastchannel'
prefix = '...'

# List all objects within a S3 bucket path
#response = s3_client.list_objects(Bucket = bucket_name, Prefix = prefix)
#for file in response['Contents']:
#    name = file['Key'].rsplit('/', 1)
#    print name

response = s3_client.list_objects(Bucket=bucket_name, Prefix=prefix)
for file in response['Contents']:
    name = file['Key'].rsplit('/', 1)
    s3_client.download_file(Bucket=bucket_name, Prefix=file['Key'], Filename='/localpath/'+name)
    print s3_client.download_file

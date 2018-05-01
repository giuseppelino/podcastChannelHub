from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

app = Flask(__name__)

#!/usr/bin/python
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
PORT_NUMBER = int(os.environ.get('PORT', 8084))

# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

  # GET
  def do_HEAD(self):
        # Send response status code
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        return
  # GET
  def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        #message = "Hello world!"
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return



def run():
  print('starting server...')

# Server settings
  # Choose port 8080, for port 80, which is normally used for a http server, you need root access
  server_address = ('0.0.0.0', PORT_NUMBER)
  httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
  print('running server...')
  httpd.serve_forever()

run()


# Config MySQL
app.config['MYSQL_HOST'] = '129.158.71.11'
app.config['MYSQL_USER'] = 'mysqladmin'
app.config['MYSQL_PASSWORD'] = 'ATB9fgPH!@'
app.config['MYSQL_DB'] = 'mydatabase'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MySQL
mysql = MySQL(app)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/', methods=['GET'])
def index():
    cur = mysql.connection.cursor()
    query = 'SELECT * from videos'
    cur.execute(query)
    data = cur.fetchall()
    for row in data:
        title=row["title"]
        description=row["description"]
        link=row["link"]

        #print "%s, %s, %s" % (row["title"], row["description"], row["link"])
    cur.close()
    #redirect(url_for('index'))
    #return render_template('home.html', data=data)
    return render_template('home.html', title=title, description=description, link=link, data=data )


class RegisterForm(Form):
        name = StringField("Name", [validators.Length(min=1, max=50)])
        lastname = StringField("Last name", [validators.Length(min=1, max=50)])
        email = StringField("Email", [validators.Length(min=1, max=50)])
        confirm = StringField("Confirm email", [validators.Length(min=1, max=50)])
        #Add assert '@oracle.com' in Email

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method =='POST' and form.validate():
        name = form.name.data
        lastname = form.lastname.data
        email = form.email.data

        # Create DictCursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, lastname, email) VALUES(%s, %s, %s)", (name, lastname, email))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now subscribed to the podcast channel', 'success')

        redirect(url_for('index'))
    return render_template('register.html', form=form)

app = Flask(__name__)

if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)

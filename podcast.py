from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_mail import Mail, Message

app = Flask(__name__)

# email server configuration -- To do : hide user and osw
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ''  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = '' # enter your email here
app.config['MAIL_PASSWORD'] = '' # enter your password here

mail = Mail(app)

# Config MySQL
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = 'mysqladmin'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'mydatabase'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MySQL
mysql = MySQL(app)

# Entry point for about.html web page
@app.route('/about')
def about():
    return render_template('about.html')

# Procedure to create and append the info for the feedback form. It will have the info of the user and the message of the feedback
class FeedbackForm(Form):
        name = StringField("Name", [validators.Length(min=1, max=50)])
        description = StringField("Description", [validators.Length(min=1, max=250)])
        email = StringField("Email", [validators.Length(min=1, max=50)])
        confirm = StringField("Confirm email", [validators.Length(min=1, max=50)])

# Entry for the procedure to call the feedback webpage
@app.route('/feedback', methods=['GET', 'POST'])
def feddback():
    # Call the procedure Feedback to be able to do the post, validate the info and send the email(feedback)
    form = FeedbackForm(request.form)
    if request.method =='POST' and form.validate():
        # Assigning the information to variables to then create the email to send the feedback
        name = form.name.data
        description = form.description.data
        email = form.email.data

        msg = Message("Feedback", recipients=[app.config['MAIL_USERNAME']])
        msg.body = "You have received a new feedback from {} <{}> Feedback  <{}>.".format(name, email, description)
        mail.send(msg)
        # Message for success
        flash('Your feedback has been sent', 'success')

        redirect(url_for('index'))
    return render_template('feedback.html', form=form)

# Entry for the procedure to call the home webpage - The main goal of this piece of code, is to go to the video table ("videos") and create the webpage dynamically
@app.route('/', methods=['GET'])
def index():
    # Go into the tabe and fetch all the information. We will create an array to load all the info and use POST to send it and render the webpage
    cur = mysql.connection.cursor()
    query = 'SELECT * from videos1'
    cur.execute(query)
    data = cur.fetchall()
    mylist =[]
    for row in data:
        mylist.append(row)
    #print(mylist)
    cur.close()
    return render_template('home.html', mylist=mylist)

# Procedure to create and append the info for the subscribe form. It will have the info to be ablel to subscribe the user to the channel
class RegisterForm(Form):
        name = StringField("Name", [validators.Length(min=1, max=50)])
        lastname = StringField("Last name", [validators.Length(min=1, max=50)])
        email = StringField("Email", [validators.Length(min=1, max=50)])
        confirm = StringField("Confirm email", [validators.Length(min=1, max=50)])
        # To do - Add assert '@oracle.com' in Email

# Entry for the procedure to call the subscribe webpage - The main goal of this piece of code, is to validate the form and insert the information of the user into the DB (table users)
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
        # Message for success
        redirect(url_for('index'))
    return render_template('register.html', form=form)

# Main entry point for the app to work
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True, host='0.0.0.0')

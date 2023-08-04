# Import Libraries 
from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import pymssql
import bcrypt
# ------------------------------------------------------------------------------



# Define app.
app = Flask(__name__)
app.config['SECRET_KEY'] = 'UUSD445xxxxaxDBB002'  # Replace with your secret key

# MSSQL Server credentials
DBuser = 'GS_User'
DBpass = 'G0S3amless'
server = '10.244.229.23'
database = '[GS-WebApplication]'

# Import the __init__.py from modules which had imported all files from the folder.
# import modules
# ------------------------------------------------------------------------------

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

def validate_user(username, password):
    conn = pymssql.connect(server=server, user=DBuser, password=DBpass, database=database)
    cursor = conn.cursor()
    cursor.execute('select PasswordHash from AspNetUsers where email = %s', (username))
    
    hashed_password = cursor.fetchone()
    cursor.close()
    conn.close()

    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
# ------------------------------------------------------------------------------


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if validate_user(username, password):
            return redirect('/dashboard')  # Redirect to the dashboard page upon successful login

        return redirect('/error')  # Redirect to the error page for invalid credentials

    return render_template('login.html', form=form)


@app.route('/dashboard')
def dashboard():
    return 'Dashboard Page'

@app.route('/error')
def error():
    return 'Invalid Credentials'


# ------------------------------------------------------------------------------


if __name__ == '__main__':
    app.run()
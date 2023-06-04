from app import app
from flask import request

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

def validate_user(username, password):
    # Establish a connection to the MSSQL Server
    conn = pymssql.connect(server=server, user=DBuser, password=DBpass, database=database)

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Execute a query to validate the user credentials
    cursor.execute('select PasswordHash from AspNetUsers where email = %s', (username))

    # Fetch the result of the query
    hashed_password = cursor.fetchone()

    # Close the cursor and the connection
    cursor.close()
    conn.close()

    # Return True if a user with matching credentials exists, False otherwise
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


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

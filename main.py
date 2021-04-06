from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'sqlproject'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '13.233.146.174'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'threatre'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/insertmovie/ - this will be the login page, we need to use both GET and POST requests
@app.route('/insertmovie/', methods=['GET', 'POST'])
def insertmovie():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'movie_id' in request.form and 'movie_name' in request.form and 'duration' in request.form and 'movie_type' in request.form and 'description' in request.form and 'hall_id' in request.form:
        # Create variables for easy access
        movie_id = request.form['movie_id']
        movie_name = request.form['movie_name']
        duration = request.form['duration']
        movie_type = request.form['movie_type']
        description = request.form['description']
        hall_id = request.form['hall_id']
        show_time=request.form['show_time']
        # Check if movies exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM movies WHERE movie_id = %s AND movie_name = %s', (movie_id, movie_name,))
        # Fetch one record and return result
        movies  = cursor.fetchone()
        if movies:
            msg = 'movie already exists!'
        elif not movie_id or not movie_name:
            msg = 'Please fill out the form!'
        else:
            # movies doesnt exists and the form data is valid, now insert new movies into movies table
            cursor.execute('INSERT INTO movies VALUES (%s, %s, %s, %s,%s,%s,%s)', (movie_id,movie_name,duration,movie_type,description,hall_id,show_time,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
        # If movies exists in movies table in out database

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

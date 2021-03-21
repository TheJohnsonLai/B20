# Required imports
import sqlite3
# g is used for database
from flask import Flask, render_template, request, g

DATABASE = './assignment3.db'

# the function get_db is from
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # Open a connection
        db = g._database = sqlite3.connect(DATABASE)
    return db

# the function query_db is from
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def query_db(query, args=(), one=False): #1=F means select all entries
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# the function make_dicts is from
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# ---------------------------------------------- Flask ------------------------------------------------

app = Flask(__name__)

# the function close_connection is from
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # Close the connection
        db.close()

@app.route('/assignments.html')
def assignments_page():
    return render_template('assignments.html')

@app.route('/calendar.html')
def calendar_page():
    return render_template('calendar.html')

@app.route('/feedback.html')
def feedback_page():
    return render_template('feedback.html')

@app.route('/index.html')
def index_page():
    return render_template('index.html')

@app.route('/lectures.html')
def lectures_page():
    return render_template('lectures.html')

@app.route('/links.html')
def links_page():
    return render_template('links.html')

@app.route('/team.html')
def team_page():
    return render_template('team.html')

@app.route('/tests.html')
def tests_page():
    return render_template('tests.html')

@app.route('/tutorials.html')
def tutorials_page():
    return render_template('tutorials.html')

# To be implemented (Student grades - view. Currently lists students, accessed in HTML by {% for item in usersH %})
@app.route('/grades.html')
def view_grades():
    db=get_db()
    # Each row from the table is placed in dictionary form
    db.row_factory = make_dicts

    users=[]
    # Inside DB are some tables. 
    for user in query_db('select * from STUDENT'):
        users.append(user)

    db.close()

    return render_template('studentgrades.html', usersH=users)

# Landing page. What will it be?
@app.route('/')
def root():
    return render_template('index.html') # Change to landing html!

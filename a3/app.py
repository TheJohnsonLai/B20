# Required imports
import sqlite3
# g is used for database
from flask import Flask, render_template, request, g
from flask import Flask, flash, redirect, render_template, request, session, abort

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
def query_db(query, args=(), one=False):  # 1=F means select all entries
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

# ---------------------------------------------- Authentication ---------------------------------------

app.secret_key = "thesecretkey"
# This stuff is yet to be decided - how to implement authentication. Cannot use SQLalchemy.
# session['VARNAME'] = VALUE
# session['user_type'] = instructor
# session['username'] = instructor1

# the function close_connection is from
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # Close the connection
        db.close()

# ---------------------------------------------- Webpages ---------------------------------------------

@app.route('/sviewgrades.html', methods=['GET', 'POST'])
def student_view_grades():
    if request.method == 'GET':
        db = get_db()
        # Each row from the table is placed in dictionary form
        db.row_factory = make_dicts
        # request.args.get('utorid')#'utorid'can be other things depend on what login page returns
        utorid = 1
        student_name = query_db(
            'select * from STUDENT where UTORID = ?', [utorid], one=True)
        name = student_name['FNAME'] + ' ' + student_name['LNAME']
        # If no such student to be implemented

        # Inside DB are some tables.
        student_grades = query_db(
            'select * from GRADES where UTORID = ?', [utorid], one=True)
        db.close()
        # return student_grades.__str__()
        return render_template('sviewgrades.html', grade=student_grades, name=name)

# To be implemented (Student grades - view. Currently lists students, accessed in HTML by {% for item in usersH %})
# Can change grades.
@app.route('/iviewgrades.html', methods=['GET', 'POST'])
def instructor_view_grades():
    if session['user_type'] != "instructor"        
        return redirect(redirect_url())
    if request.method == 'GET':
        db = get_db()
        # Each row from the table is placed in dictionary form
        db.row_factory = make_dicts
        students = []
        # Inside DB are some tables.
        for item in query_db('select * from STUDENT NATURAL JOIN GRADES'):
            students.append(item)
        db.close()
        
        return render_template('iviewgrades.html', studentH=students)
    else:  # Work in Progress - For Instructor to enter marks
        # request.form['grade']
        # request.form['examname']
        # request.form['utorid']
        try:
            db = get_db()
            db.execute('UPDATE GRADES SET ?=? WHERE UTORID=?', [examname], [grade], [utorid])
            db.close()

            return render_template('iviewgrades.html')
        except db.Error as err:
            return redirect(redirect_url())
        finally:
            db.close()

# Instructor views feedback, removes feedback
@app.route('/iviewfeedback.html', methods=['GET', 'POST'])
def instructor_view_feedback():
    if session['user_type'] != "instructor"        
        return redirect(redirect_url())
    db = get_db()
    # Each row from the table is placed in dictionary form
    db.row_factory = make_dicts
    feedback = []
    # Sample username from session (To be implemented)
    session['username'] = "instructor1"
    for item in query_db('select FA, FB, FC, FD from FEEDBACK NATURAL JOIN USER WHERE USERNAME LIKE ?', [session['username']]):
        feedback.append(item)
    db.close()

    # return fb.__str__()
    return render_template('iviewfeedback.html', feedbackH=feedback)

# Instructor views remark requests, removes remark requests
@app.route('/iviewremarks.html', methods=['GET', 'POST'])
def instructor_view_remarks():
    if session['user_type'] != "instructor"        
        return redirect(redirect_url())
    db = get_db()
    # Each row from the table is placed in dictionary form
    db.row_factory = make_dicts
    remarks = []
    # Inside DB are some tables.
    for item in query_db('select UTORID, FNAME, LNAME, EXAMNAME, COMMENT FROM REMARKS NATURAL JOIN STUDENT'):
        remarks.append(item)
    db.close()
    return render_template('iviewremarks.html', remarksH=remarks)

# Redirect back to the previous page (if the user attempts to access something bad)
# From https://flask.palletsprojects.com/en/1.1.x/reqcontext/
def redirect_url(default='index.html'):
    return request.args.get('next') or request.referrer or url_for(default)
    # Use >> return redirect(redirect_url()) << In function call

# Landing page. What will it be?
@app.route('/')
def root():
    return render_template('index.html')  # Change to landing html!

# Instructor Panel
@app.route('/instructorpanel.html')
def instructor_panel_page():
    return render_template('instructorpanel.html')

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
    # Testing - Instructor View (Remove later)
    session['user_type'] = "instructor"
    return render_template('links.html', user_type=session['user_type'])

@app.route('/team.html')
def team_page():
    return render_template('team.html')

@app.route('/tests.html')
def tests_page():
    return render_template('tests.html')

@app.route('/tutorials.html')
def tutorials_page():
    return render_template('tutorials.html')

# -------------------------------------------- Port --------------------------------------

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

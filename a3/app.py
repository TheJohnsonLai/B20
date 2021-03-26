# Required imports
import sqlite3, time
# g is used for database, not all will be used
from flask import Flask, render_template, request, g, redirect, session, url_for, abort

DATABASE = './assignment3.db'

# the function get_db is from
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # Open a connection
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
        db.row_factory = make_dicts
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

# route for login webpage
@app.route('/login', methods=['GET', 'POST'])
def login():
    session['username'] = "guest"
    session['user_type'] = "guest"
    error = None
    # TODO: query database and story usernames and password in a dict
    # if request.method == 'GET':

    if request.method == 'POST':
        if request.form['username'] != 'anna.b' or request.form['password'] != '123': #placeholder credentials (will integrate with database)
            error = "Username or password incorrect."
        else:
            return redirect(url_for('./index.html'))
    return render_template('login.html', error=error)


@app.route('/student.html', methods=['GET', 'POST'])
def student():
    #check the status of user
    if session['user_type'] != "student": 
        return redirect(redirect_url())

    db = get_db()
    # Each row from the table is placed in dictionary form
    db.row_factory = make_dicts
    # request.args.get('utorid')#'utorid'can be other things depend on what login page returns
    utorid = 1
    student_name = query_db('select * from STUDENT where UTORID = ?', [utorid], one=True)
    name = student_name['FNAME'] + ' ' + student_name['LNAME']
    section = student_name['SECTION']
    student_grades = query_db('select * from GRADES where UTORID = ?', [utorid], one=True)

    # Student grade can be found.
    if request.method == 'POST' and request.form['formName'] == "remark": #remark submitted
        comment = request.form['explain']
        created = int(time.time())
        examname = request.form['remark_area']
        #update database
        db.execute("INSERT INTO REMARKS VALUES (?, ?, ?, ?)",[1, examname, comment, created])
        db.commit()

    elif request.method == 'POST' and request.form['formName'] == "feedback": #feedback submitted
        fa = request.form['FA']
        fb = request.form['FB']
        fc = request.form['FC']
        fd = request.form['FD']
        created = int(time.time())
        #update database
        db.execute("INSERT INTO FEEDBACK VALUES (?, ?, ?, ?, ?, ?)",[section, fa, fb, fc, fd, created])
        db.commit()
    
    db.close()
    return render_template('student.html', grade=student_grades, name=name, section = section)

# Instructor View - All Grades
@app.route('/iviewgrades.html', methods=['GET', 'POST'])
def instructor_view_grades():
    if session['user_type'] != "instructor":       
        return redirect(redirect_url())

    db = get_db()

    if (request.method == 'POST'):
        try:
            # Submit Marks button calls db.execute
            grade = request.form['new-grade']
            examname = request.form['list-examname']
            utorid = request.form["list-utorid"]
            # Table Column names cannot be accessed normally
            sql = """UPDATE GRADES SET {} = {} WHERE UTORID = '{}'""".format(examname, grade, utorid)
            cur = db.cursor()
            cur.execute(sql)
            db.commit
        except:
            print ("Error with SQL statement. (I-Grades)")
    
    students = query_db('select * from STUDENT NATURAL JOIN GRADES')  
    ids = query_db('select UTORID from STUDENT')
    db.close()
            
    return render_template('iviewgrades.html', studentH=students, ulist=ids, elist=get_exam_names())

# Instructor views feedback, removes feedback
@app.route('/iviewfeedback.html', methods=['GET', 'POST'])
def instructor_view_feedback():
    if session['user_type'] != "instructor":
        return redirect(redirect_url())

    session['username'] = "instructor1" # To be changed later, when authentication is added.

    db = get_db()
    if (request.method == 'POST'):
        try:
            unixtime = request.form['created-date']
            sql = """DELETE FROM FEEDBACK WHERE CREATED = {}""".format(unixtime)
            cur = db.cursor()
            cur.execute(sql)
            db.commit
        except:
            print ("Error with SQL statement. (I-Feedback)")

    feedback = []
    # View feedback that is directed towards this user (instructor)
    for item in query_db('select FA, FB, FC, FD, CREATED from FEEDBACK NATURAL JOIN USER WHERE USERNAME LIKE ?', [session['username']]):
        feedback.append(item)
    db.close()

    return render_template('iviewfeedback.html', feedbackH=feedback)

# Instructor views remark requests, removes remark requests
@app.route('/iviewremarks.html', methods=['GET', 'POST'])
def instructor_view_remarks():
    if session['user_type'] != "instructor": 
        return redirect(redirect_url())

    db=get_db()
    if (request.method == 'POST'):
        try:
            unixtime = request.form['created-date']
            sql = """DELETE FROM REMARKS WHERE CREATED = {}""".format(unixtime)
            cur = db.cursor()
            cur.execute(sql)
            db.commit
        except:
            print ("Error with SQL statement. (Remarks)")

    remarks = []
    # View remark requests.
    for item in query_db('select UTORID, FNAME, LNAME, EXAMNAME, COMMENT, CREATED FROM REMARKS NATURAL JOIN STUDENT'):
        remarks.append(item)
    db.close()

    return render_template('iviewremarks.html', remarksH=remarks)

# Redirect back to the previous page (if the user attempts to access something bad)
# From https://flask.palletsprojects.com/en/1.1.x/reqcontext/
def redirect_url(default='/'):
    return request.args.get('next') or request.referrer or url_for(default)
    # Use >> return redirect(redirect_url()) << In function call

# Landing page. What will it be?
@app.route('/')
def root():
    return render_template('login.html')  # Change to landing html!

# Instructor Panel
@app.route('/instructorpanel.html')
def instructor_panel_page():
    if session['user_type'] != "instructor":
        return redirect(redirect_url())
    return render_template('instructorpanel.html', usertype=session['user_type'])

@app.route('/assignments.html')
def assignments_page():
    return render_template('assignments.html', usertype=session['user_type'])

@app.route('/calendar.html')
def calendar_page():
    return render_template('calendar.html', usertype=session['user_type'])

@app.route('/index.html')
def index_page():
    return render_template('index.html', usertype=session['user_type'])

@app.route('/lectures.html')
def lectures_page():
    return render_template('lectures.html', usertype=session['user_type'])

@app.route('/links.html')
def links_page():
    # Testing - Applies Instructor View (Remove later)
    session['user_type'] = "instructor"
    return render_template('links.html', user_type=session['user_type'])

@app.route('/team.html')
def team_page():
    # Testing - Applies Student View (Remove later)
    session['user_type'] = "student"
    return render_template('team.html', usertype=session['user_type'])

@app.route('/tests.html')
def tests_page():
    return render_template('tests.html', usertype=session['user_type'])

@app.route('/tutorials.html')
def tutorials_page():
    return render_template('tutorials.html', usertype=session['user_type'])

@app.route('/logout')
def logout_redirect():
    session['username'] = ''
    session['user_type'] = 'guest'
    return render_template('login.html')

# Bad links redirect to the login page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('login.html'), 404

# Runs after a request, clears cache (Development purposes)
@app.after_request
def add_header(response):
    # Sustains cache (static files) for 300 seconds
    response.headers['Cache-Control'] = 'public, max-age=300'
    return response

# -------------------------------------------- Helper Functions --------------------------

# returns exam & assignment names
def get_exam_names():
    exams = ["A1","A2","A3","T1","T2","T3","FINAL"]
    return exams

# -------------------------------------------- Port --------------------------------------

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    app.debug = True
    app.run()
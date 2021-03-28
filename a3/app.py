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

def log_the_user_in(username):
    return render_template('index.html')

def valid_login(username, password):
    user = query_db('SELECT * from USER where username = ? and password = ?', [username, password], one=True)
    if user is None:
        return False
    else:
        return True

# ---------------------------------------------- Flask ------------------------------------------------

app = Flask(__name__)
app.secret_key = "thesecretkey"

# the function close_connection is from
# https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # Close the connection
        db.close()

# ---------------------------------------------- Authentication ---------------------------------------

# Login route
@app.route("/")
@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'The username/password you’ve entered is incorrect.'

    return render_template('login.html', error=error)

# Logout route redirects to Login page
@app.route('/logout')
def logout_redirect():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('login'))

# Bad links redirect to the login page
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('login')), 404

# ---------------------------------------------- Webpages ---------------------------------------------

@app.route('/student.html', methods=['GET', 'POST'])
def student():
    #check the status of user
    #if session['user_type'] != "student": 
        #return redirect(redirect_url())

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
            # Table Column names cannot be accessed normally, format within triple quotes
            sql = """UPDATE GRADES SET {} = {} WHERE UTORID = '{}'""".format(examname, grade, utorid)
            db.execute(sql)
            db.commit
        except:
            print ("Error with SQL statement. (I-Grades)")

    sql = """select * from STUDENT NATURAL JOIN GRADES where section = 
            (select section from instructor i natural join user u where u.username = '{}')""".format(session['username'])
    students = query_db(sql)  
    sql = """select UTORID from STUDENT where section = 
            (select section from instructor i natural join user u where u.username = '{}')""".format(session['username'])
    ids = query_db(sql)
    db.close()
            
    return render_template('iviewgrades.html', studentH=students, ulist=ids, elist=get_exam_names())

# Instructor View - Feedback, can remove feedback
@app.route('/iviewfeedback.html', methods=['GET', 'POST'])
def instructor_view_feedback():
    if session['user_type'] != "instructor":
        return redirect(redirect_url())

    db = get_db()
    
    if (request.method == 'POST'):
        try:
            unixtime = request.form['created-date']
            sql = """DELETE FROM FEEDBACK WHERE CREATED = {}""".format(unixtime)
            db.execute(sql)
            db.commit
        except:
            print ("Error with SQL statement. (I-Feedback)")

    feedback = []
    sql = """select DISTINCT FA, FB, FC, FD, CREATED from FEEDBACK NATURAL JOIN USER WHERE SECTION = 
            (select section from instructor i natural join user u where u.username = '{}') order by CREATED""".format(session['username'])
    # View feedback that is directed towards this course section
    feedback = query_db(sql)
    db.close()

    return render_template('iviewfeedback.html', feedbackH=feedback)

# Instructor View - Remark Requests, can remove remark requests
@app.route('/iviewremarks.html', methods=['GET', 'POST'])
def instructor_view_remarks():
    if session['user_type'] != "instructor": 
        return redirect(redirect_url())

    db=get_db()

    if (request.method == 'POST'):
        try:
            unixtime = request.form['created-date']
            sql = """DELETE FROM REMARKS WHERE CREATED = {}""".format(unixtime)
            db.execute(sql)
            db.commit
        except:
            print ("Error with SQL statement. (Remarks)")

    remarks = []
    # View remark requests.
    sql = """select UTORID, FNAME, LNAME, EXAMNAME, COMMENT, CREATED FROM REMARKS NATURAL JOIN STUDENT where section = 
            (select section from instructor i natural join user u where u.username = '{}') order by CREATED""".format(session['username'])
    for item in query_db(sql):
        remarks.append(item)
    db.close()

    return render_template('iviewremarks.html', remarksH=remarks)

# Redirect back to the previous page (if the user attempts to access something bad)
# From https://flask.palletsprojects.com/en/1.1.x/reqcontext/
def redirect_url(default='root'):
    return request.args.get('next') or request.referrer or url_for(default)
    # Use >> return redirect(redirect_url()) << In function call

# Landing page. What will it be?
@app.route('/')
def root():
    return render_template('index.html')  # Change to landing html!

# Instructor Panel
@app.route('/instructorpanel.html')
def instructor_panel_page():
    if session['user_type'] != "instructor":
        print("Only instructors can access this page!" + redirect_url())
        return redirect(redirect_url())
    return render_template('instructorpanel.html', user_type=session['user_type'])

@app.route('/assignments.html')
def assignments_page():
    return render_template('assignments.html', user_type=session['user_type'])

@app.route('/calendar.html')
def calendar_page():
    return render_template('calendar.html', user_type=session['user_type'])

@app.route('/index.html')
def index_page():
    return render_template('index.html', user_type=session['user_type'])

@app.route('/lectures.html')
def lectures_page():
    return render_template('lectures.html', user_type=session['user_type'])

@app.route('/links.html')
def links_page():
    # Testing - Applies Instructor View (Remove later)
    session['user_type'] = "instructor"
    session['username'] = "instructor1"
    return render_template('links.html', user_type=session['user_type'])

@app.route('/team.html')
def team_page():
    # Testing - Applies Student View (Remove later)
    session['user_type'] = "student"
    return render_template('team.html', user_type=session['user_type'])

@app.route('/tests.html')
def tests_page():
    return render_template('tests.html', user_type=session['user_type'])

@app.route('/tutorials.html')
def tutorials_page():
    return render_template('tutorials.html', user_type=session['user_type'])

# Runs after a request, clears cache (Development purposes)
@app.after_request
def add_header(response):
    # Sustains cache (static files) for 300 seconds
    response.headers['Cache-Control'] = 'public, max-age=600'
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
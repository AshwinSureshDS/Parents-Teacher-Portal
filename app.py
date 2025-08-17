"""
from flask import Flask, render_template, request, redirect, url_for, g, session, jsonify
import sqlite3

app = Flask(__name__)

# Secret key for session management (optional for security)
app.secret_key = 'your_secret_key'

def get_db():
  if 'db' not in g:
    g.db = sqlite3.connect('tiny_wonders.db')
  return g.db

@app.teardown_appcontext
def close_db(error):
  if 'db' not in g:
    return
  db = g.pop('db')
  db.close()


@app.route('/', methods=['GET', 'POST'])  # Allow both GET and POST requests
def login():
    db = get_db()
    error = None
    if request.method == 'POST':
        roll_no = request.form['roll_no']
        password = request.form['password']
        user_type = 'Teacher' if request.form.get('toggle') else 'Parent'

        cursor = db.cursor()
        cursor.execute("SELECT * FROM parents WHERE roll_no = ? AND password = ? AND user_type = ?", (roll_no, password, user_type))
        user = cursor.fetchone()

        if user is None:
            error = 'Invalid credentials. Please try again.'
        else:
            # Debugging: Print user details
            print(f"User found: {user}")  

            session['user_id'] = user[1]  # Assuming roll_no is at index 1
            session['user_type'] = user[4]  # Assuming user_type is at index 4
            print(f"Session Data: {session}")  # Debugging

            return redirect(url_for('home'))  # Redirect directly to home

    return render_template('login.html', error=error)

@app.route('/login_success')
def login_success():
  return redirect(url_for('home')) #return "<h1></h1>"  # You can customize this success page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db = get_db()
    c = db.cursor()
    error = None

    if request.method == 'POST':
        username = request.form['name']
        roll_no_or_teacher_id = request.form['roll_no']  # This will be roll_no for parents and teacher_id for teachers
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        #user_type = 'Teacher' if request.form else 'Parent'
        user_type = 'Teacher' if request.form.get('toggle') else 'Parent'


        # Validation checks (add more as needed)
        if not username:
            error = 'Username is required'
        elif not roll_no_or_teacher_id:
            error = 'Roll Number/Teacher ID is required'
        elif not password or not confirm_password:
            error = 'Password and confirm password are required'
        elif password != confirm_password:
            error = 'Passwords don\'t match'
        else:
            # Check if email already exists (optional)
            if user_type == 'Parent':
                c.execute("SELECT * FROM parents WHERE email = ?", (email,))
            else:
                c.execute("SELECT * FROM teachers WHERE email = ?", (email,))
            if c.fetchone() is not None:
                error = 'Email address already exists'

        if error is None:
            # Insert user data if validation passes
            if user_type == 'Parent':
                c.execute("INSERT INTO parents (username, roll_no, email, password, user_type) VALUES (?, ?, ?, ?, ?)", 
                          (username, roll_no_or_teacher_id, email, password, user_type))
            else:
                c.execute("INSERT INTO teachers (username, teacher_id, email, password, user_type) VALUES (?, ?, ?, ?, ?)", 
                          (username, roll_no_or_teacher_id, email, password, user_type))
            db.commit()
            return redirect(url_for('login_success'))  # Redirect to success page

    return render_template('sign_up.html', error=error)

@app.route('/logout')
def logout():
    # Clear session data (important for secure logout)
    session.clear()
    
    # Redirect to the login page
    return redirect(url_for('login'))


def get_current_user():
    if 'user_id' in session:
        db = get_db()
        cursor = db.cursor()

        # Check both tables for the user
        cursor.execute("SELECT * FROM parents WHERE roll_no = ?", (session['user_id'],))
        user = cursor.fetchone()
        
        if not user:
            cursor.execute("SELECT * FROM teachers WHERE teacher_id = ?", (session['user_id'],))
            user = cursor.fetchone()
        
        return user
    return None

def get_contact_details(roll_no):
    conn = sqlite3.connect('tiny_wonders.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contact_details WHERE roll_no = ?", (roll_no,))
    contact_details = cursor.fetchone()

    conn.close()
    return contact_details


def get_timetable():
    conn = sqlite3.connect('tiny_wonders.db')
    cursor = conn.cursor()

    # Fetch timetable data
    cursor.execute("SELECT * FROM timetable")
    data = cursor.fetchall()
    conn.close()

    return data 

def get_report_card(roll_no):
    conn = sqlite3.connect('tiny_wonders.db')
    cursor = conn.cursor()

    # Fetch report card data for the logged-in user
    cursor.execute("SELECT subject, marks FROM report_card WHERE roll_no = ?", (roll_no,))
    report_card_data = cursor.fetchall()

    conn.close()
    return report_card_data




@app.route('/home')
def home():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))
    
    roll_no = current_user[1]  # Assuming roll_no is at index 1 in your `parents`table    
    data = get_timetable()
    report_card_data = get_report_card(roll_no)
    contact_details = get_contact_details(roll_no)
    notices = get_notices()
    return render_template('parent copy 3.html',
                           current_user=current_user,
                           data=data,
                           report_card_data=report_card_data,
                           contact_details=contact_details)


@app.route('/get_notices')
def get_notices():
    try:
        conn = sqlite3.connect('tiny_wonders.db')
        cursor = conn.cursor()

        cursor.execute("SELECT id, title, content, date_posted FROM notices")
        notices_data = cursor.fetchall()

        notices = []
        for row in notices_data:
            notices.append({
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'date': row[3]
            })

        conn.close()
        return jsonify(notices)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to fetch notices'}), 500



if __name__ == '__main__':
  app.run(debug=True)"
"""
from flask import Flask, render_template, request, redirect, url_for, g, session, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Secret key for session management (optional for security)
app.secret_key = 'your_secret_key'

def get_db():
  if 'db' not in g:
    g.db = sqlite3.connect('tiny_wonders.db')
  return g.db

@app.teardown_appcontext
def close_db(error):
  if 'db' not in g:
    return
  db = g.pop('db')
  db.close()

@app.route('/', methods=['GET', 'POST'])
def login():
    session.clear()  # Ensures old session data doesn't interfere
    db = get_db()
    error = None

    if request.method == 'POST':
        roll_no = request.form['roll_no']
        password = request.form['password']
        user_type = request.form['user_type']

        print(f"Received Data - Roll No: {roll_no}, Password: {password}, User Type: {user_type}")  # Debugging

        cursor = db.cursor()
        if user_type == 'Parent':
            cursor.execute("SELECT * FROM parents WHERE roll_no = ? AND password = ? AND user_type = ?", 
                           (roll_no, password, user_type))
        else:
            cursor.execute("SELECT * FROM teachers WHERE teacher_id = ? AND password = ? AND user_type = ?", 
                           (roll_no, password, user_type))

        user = cursor.fetchone()

        if user is None:
            error = 'Invalid credentials. Please try again.'
        else:
            print(f"User found: {user}")  # Debugging
            session['user_id'] = user[1]  # Assuming roll_no/teacher_id is at index 1
            session['user_type'] = user[4]  # Assuming user_type is at index 4
            print(f"Session Data: {session}")  # Debugging

            if session['user_type'] == 'Teacher':
                return redirect(url_for('teacher_home'))
            else:
                return redirect(url_for('home'))

    return render_template('login.html', error=error)


@app.route('/teacher_home')
def teacher_home():
    current_user = get_current_user()
    print(f"Current User: {current_user}")  # Debugging
    print(f"Session User Type: {session.get('user_type')}")  # Debugging
    if not current_user or session['user_type'] != 'Teacher':
        return redirect(url_for('login'))

    data = get_timetable()  # Sample data retrieval for teachers
    notices = get_notices()
    return render_template('teachers copy 2.html',
                           current_user=current_user,
                           data=data,
                           notices=notices)



@app.route('/login_success')
def login_success():
  return redirect(url_for('home'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    db = get_db()
    c = db.cursor()
    error = None

    if request.method == 'POST':
        username = request.form['name']
        roll_no_or_teacher_id = request.form['roll_no']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        user_type = 'Teacher' if request.form.get('toggle') else 'Parent'

        if not username:
            error = 'Username is required'
        elif not roll_no_or_teacher_id:
            error = 'Roll Number/Teacher ID is required'
        elif not password or not confirm_password:
            error = 'Password and confirm password are required'
        elif password != confirm_password:
            error = 'Passwords don\'t match'
        else:
            if user_type == 'Parent':
                c.execute("SELECT * FROM parents WHERE email = ?", (email,))
            else:
                c.execute("SELECT * FROM teachers WHERE email = ?", (email,))
            if c.fetchone() is not None:
                error = 'Email address already exists'

        if error is None:
            if user_type == 'Parent':
                c.execute("INSERT INTO parents (username, roll_no, email, password, user_type) VALUES (?, ?, ?, ?, ?)", 
                          (username, roll_no_or_teacher_id, email, password, user_type))
            else:
                c.execute("INSERT INTO teachers (username, teacher_id, email, password, user_type) VALUES (?, ?, ?, ?, ?)", 
                          (username, roll_no_or_teacher_id, email, password, user_type))
            db.commit()
            return redirect(url_for('login_success'))

    return render_template('sign_up.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

def get_current_user():
    if 'user_id' in session:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM parents WHERE roll_no = ?", (session['user_id'],))
        user = cursor.fetchone()
        if not user:
            cursor.execute("SELECT * FROM teachers WHERE teacher_id = ?", (session['user_id'],))
            user = cursor.fetchone()
        return user
    return None

def get_contact_details(roll_no):
    conn = sqlite3.connect('tiny_wonders.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contact_details WHERE roll_no = ?", (roll_no,))
    contact_details = cursor.fetchone()

    conn.close()
    return contact_details

def get_timetable():
    conn = sqlite3.connect('tiny_wonders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timetable")
    data = cursor.fetchall()
    conn.close()
    return data

def get_report_card(roll_no):
    conn = sqlite3.connect('tiny_wonders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT subject, marks FROM report_card WHERE roll_no = ?", (roll_no,))
    report_card_data = cursor.fetchall()
    conn.close()
    return report_card_data

@app.route('/home')
def home():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('login'))

    roll_no = current_user[1]
    data = get_timetable()
    report_card_data = get_report_card(roll_no)
    contact_details = get_contact_details(roll_no)
    notices = get_notices()
    return render_template('parent copy 3.html',
                           current_user=current_user,
                           data=data,
                           report_card_data=report_card_data,
                           contact_details=contact_details)
@app.route('/create_notice', methods=['POST'])
def create_notice():
    try:
        data = request.get_json()
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return jsonify({'error': 'Title and content are required'}), 400

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Correctly formatted date

        conn = sqlite3.connect('tiny_wonders.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO notices (title, content, date_posted) VALUES (?, ?, ?)",
            (title, content, now)  # Correctly passing `now` as `date_posted`
        )

        conn.commit()
        conn.close()

        return jsonify({'success': True, 'message': 'Notice created successfully'})

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Database error occurred'}), 500
    
@app.route('/get_notices')
def get_notices():
    try:
        conn = sqlite3.connect('tiny_wonders.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, content, date_posted FROM notices")
        notices_data = cursor.fetchall()

        notices = []
        for row in notices_data:
            notices.append({
                'id': row[0],
                'title': row[1],
                'content': row[2],
                'date': row[3]
            })

        conn.close()
        return jsonify(notices)

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return jsonify({'error': 'Failed to fetch notices'}), 500

if __name__ == '__main__':
  app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management

def init_db():
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            notes TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    # Get all attendance records ordered by date
    c.execute('SELECT * FROM attendance ORDER BY date DESC')
    attendance_records = c.fetchall()
    
    conn.close()
    return render_template('index.html', attendance_records=attendance_records)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        
        if user:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    if 'username' not in session:
        return redirect(url_for('login'))
    date = request.form.get('date')
    status = request.form.get('status')
    notes = request.form.get('notes')
    
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    # Check if attendance already exists for this date
    c.execute('SELECT id FROM attendance WHERE date = ?', (date,))
    existing = c.fetchone()
    
    if existing:
        c.execute('UPDATE attendance SET status = ?, notes = ? WHERE date = ?',
                 (status, notes, date))
    else:
        c.execute('INSERT INTO attendance (date, status, notes) VALUES (?, ?, ?)',
                 (date, status, notes))
    
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
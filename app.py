"""
Smart Attendance System Using Face Recognition
Final Year Engineering Project

This application provides:
- Admin/Faculty login system
- Student registration with face capture
- Real-time face detection attendance
- Attendance viewing and reporting
- CSV/Excel export functionality

Flow for Viva:
1. Admin logs in with credentials
2. Admin registers students by capturing their faces
3. For attendance: Start camera, faces are detected
4. System marks attendance with timestamp
5. View and export reports as needed
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response
import cv2
import numpy as np
import os
import sqlite3
import pandas as pd
from datetime import datetime, date
from functools import wraps
import base64
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)
app.secret_key = 'smart_attendance_system_secret_key'

# Configuration
DATABASE = 'attendance.db'
UPLOAD_FOLDER = 'static/student_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load Haar Cascade for face detection
cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(cascade_path)

# Initialize database
def init_db():
    """Initialize database tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Users table (Admin/Faculty)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            role TEXT DEFAULT 'admin'
        )
    ''')
    
    # Students table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            year TEXT NOT NULL,
            section TEXT NOT NULL,
            image_path TEXT,
            encoding_data BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Attendance table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            date DATE NOT NULL,
            time TIME NOT NULL,
            status TEXT DEFAULT 'Present',
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    ''')
    
    # Create default admin user
    try:
        cursor.execute("INSERT INTO users (username, password, name, role) VALUES (?, ?, ?, ?)",
                       ('admin', 'admin123', 'Administrator', 'admin'))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    
    conn.close()

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTHENTICATION ROUTES ====================

@app.route('/')
def index():
    """Home page redirects to login or dashboard"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin/Faculty login page"""
    error = None
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?',
                          (username, password)).fetchone()
        conn.close()
        
        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['name'] = user['name']
            session['role'] = user['role']
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password!'
    
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

# ==================== DASHBOARD ROUTES ====================

@app.route('/dashboard')
@login_required
def dashboard():
    """Admin Dashboard with statistics"""
    conn = get_db_connection()
    
    # Get total students
    total_students = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    
    # Get today's date and attendance
    today = date.today().strftime('%Y-%m-%d')
    today_present = conn.execute(
        'SELECT COUNT(DISTINCT student_id) FROM attendance WHERE date = ?',
        (today,)
    ).fetchone()[0]
    
    # Calculate absent (total students - present today)
    today_absent = total_students - today_present
    
    # Get current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    conn.close()
    
    return render_template('dashboard.html',
                           total_students=total_students,
                           today_present=today_present,
                           today_absent=today_absent,
                           current_datetime=current_datetime,
                           user_name=session['name'])

# ==================== STUDENT REGISTRATION ROUTES ====================

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register_student():
    """Student registration page"""
    message = None
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        department = request.form['department']
        year = request.form['year']
        section = request.form['section']
        image_data = request.form.get('image_data')
        
        conn = get_db_connection()
        
        # Check if student already exists
        existing = conn.execute('SELECT * FROM students WHERE student_id = ?', (student_id,)).fetchone()
        
        if existing:
            message = {'type': 'error', 'text': 'Student with this ID already exists!'}
        elif not image_data:
            message = {'type': 'error', 'text': 'Please capture face image!'}
        else:
            # Save image
            image_path = f'student_images/{student_id}.jpg'
            full_path = os.path.join('static', image_path)
            
            # Decode base64 image
            header, encoded = image_data.split(',', 1)
            with open(full_path, 'wb') as f:
                f.write(base64.b64decode(encoded))
            
            # Create face encoding using OpenCV
            image = cv2.imread(full_path)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Store face encoding
            encoding_data = None
            if len(faces) > 0:
                x, y, w, h = faces[0]
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (100, 100))
                encoding_data = face_roi.tobytes()
            
            # Insert into database
            conn.execute('''
                INSERT INTO students (student_id, name, department, year, section, image_path, encoding_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, name, department, year, section, image_path, encoding_data))
            conn.commit()
            message = {'type': 'success', 'text': f'Student {name} registered successfully!'}
        
        conn.close()
    
    return render_template('register.html', message=message)

# ==================== ATTENDANCE ROUTES ====================

@app.route('/attendance')
@login_required
def attendance():
    """Take attendance page"""
    return render_template('attendance.html')

@app.route('/get_attendance_status')
@login_required
def get_attendance_status():
    """Get current attendance status for today"""
    conn = get_db_connection()
    today = date.today().strftime('%Y-%m-%d')
    
    # Get total students count
    total_students = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    
    present_students = conn.execute('''
        SELECT * FROM attendance WHERE date = ? ORDER BY time DESC
    ''', (today,)).fetchall()
    
    conn.close()
    
    return jsonify({
        'date': today,
        'total_students': total_students,
        'present_count': len(present_students),
        'students': [dict(row) for row in present_students]
    })

# Global variables for camera control
camera = None
is_camera_running = False

def generate_frames():
    """Generate frames for video streaming with face detection"""
    global camera, is_camera_running
    
    if camera is None:
        camera = cv2.VideoCapture(0)
        camera.set(3, 640)
        camera.set(4, 480)
    
    is_camera_running = True
    
    # Load registered students
    conn = get_db_connection()
    students = conn.execute('SELECT student_id, name, image_path, encoding_data FROM students').fetchall()
    conn.close()
    
    # Create a simple face matching system using LBPH
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    # Train recognizer with registered faces
    train_images = []
    train_labels = []
    label_to_student = {}
    
    for idx, student in enumerate(students):
        if student['encoding_data']:
            nparr = np.frombuffer(student['encoding_data'], np.uint8)
            face_img = nparr.reshape((100, 100))
            train_images.append(face_img)
            train_labels.append(idx)
            label_to_student[idx] = {'name': student['name'], 'id': student['student_id']}
    
    if train_images:
        recognizer.train(train_images, np.array(train_labels))
    
    marked_today = set()
    today = date.today().strftime('%Y-%m-%d')
    
    # Load already marked attendance for today
    conn = get_db_connection()
    marked = conn.execute('SELECT student_id FROM attendance WHERE date = ?', (today,)).fetchall()
    conn.close()
    for m in marked:
        marked_today.add(m['student_id'])
    
    frame_count = 0
    process_every_n_frames = 3
    
    while is_camera_running:
        success, frame = camera.read()
        
        if not success:
            break
        
        frame_count += 1
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Process faces for attendance (every few frames)
        if frame_count % process_every_n_frames == 0:
            for (x, y, w, h) in faces:
                # Extract and recognize face
                face_roi = gray[y:y+h, x:x+w]
                face_roi = cv2.resize(face_roi, (100, 100))
                
                if train_images:
                    label, confidence = recognizer.predict(face_roi)
                    
                    # Lower confidence = better match
                    if confidence < 100:  # Threshold for recognition
                        student_info = label_to_student.get(label)
                        if student_info:
                            student_id = student_info['id']
                            student_name = student_info['name']
                            
                            # Mark attendance if not already marked today
                            if student_id and student_id not in marked_today:
                                conn = get_db_connection()
                                dept_info = conn.execute(
                                    'SELECT department FROM students WHERE student_id = ?',
                                    (student_id,)
                                ).fetchone()
                                dept = dept_info['department'] if dept_info else 'Unknown'
                                
                                current_time = datetime.now().strftime('%H:%M:%S')
                                conn.execute('''
                                    INSERT INTO attendance (student_id, name, department, date, time, status)
                                    VALUES (?, ?, ?, ?, ?, 'Present')
                                ''', (student_id, student_name, dept, today, current_time))
                                conn.commit()
                                conn.close()
                                marked_today.add(student_id)
                                
                                # Draw green box for recognized face
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                cv2.putText(frame, f"{student_name}", (x, y-10),
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                            else:
                                # Already marked - show in yellow
                                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
                                cv2.putText(frame, f"{student_name} (Already Marked)", (x, y-10),
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                        else:
                            # Unknown face - red box
                            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                            cv2.putText(frame, "Unknown", (x, y-10),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    else:
                        # Low confidence - red box
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        cv2.putText(frame, "Unknown", (x, y-10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                else:
                    # No trained faces - just detect without recognition
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            else:
                # No face detected
                pass
        
        # Add watermark
        cv2.putText(frame, 'Smart Attendance System', (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f'Date: {today}', (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
@login_required
def video_feed():
    """Video streaming route"""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_camera', methods=['POST'])
@login_required
def start_camera():
    """Start the camera"""
    global camera, is_camera_running
    if not is_camera_running:
        camera = cv2.VideoCapture(0)
        is_camera_running = True
    return jsonify({'status': 'success', 'message': 'Camera started'})

@app.route('/stop_camera', methods=['POST'])
@login_required
def stop_camera():
    """Stop the camera"""
    global camera, is_camera_running
    is_camera_running = False
    if camera:
        camera.release()
        camera = None
    return jsonify({'status': 'success', 'message': 'Camera stopped'})

# ==================== VIEW ATTENDANCE ROUTES ====================

@app.route('/view_attendance', methods=['GET', 'POST'])
@login_required
def view_attendance():
    """View attendance records with filters"""
    conn = get_db_connection()
    
    # Get filter parameters
    filter_date = request.args.get('date', '')
    filter_department = request.args.get('department', '')
    filter_section = request.args.get('section', '')
    
    query = 'SELECT * FROM attendance WHERE 1=1'
    params = []
    
    if filter_date:
        query += ' AND date = ?'
        params.append(filter_date)
    
    if filter_department:
        query += ' AND department = ?'
        params.append(filter_department)
    
    if filter_section:
        query += " AND student_id LIKE ?"
        params.append(f'%{filter_section}%')
    
    query += ' ORDER BY date DESC, time DESC'
    
    attendance_records = conn.execute(query, params).fetchall()
    
    # Get departments for filter dropdown
    departments = conn.execute('SELECT DISTINCT department FROM students').fetchall()
    
    # Calculate stats
    total_records = len(attendance_records)
    
    conn.close()
    
    return render_template('view_attendance.html',
                         records=attendance_records,
                         departments=departments,
                         filter_date=filter_date,
                         filter_department=filter_department,
                         filter_section=filter_section,
                         total_records=total_records)

# ==================== REPORTS ROUTES ====================

@app.route('/reports', methods=['GET', 'POST'])
@login_required
def reports():
    """Reports page"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        report_type = request.form.get('report_type')
        month = request.form.get('month')
        export_format = request.form.get('export_format', 'csv')
        
        if report_type == 'daily':
            # Daily report
            records = conn.execute('''
                SELECT * FROM attendance WHERE date = ?
            ''', (month,)).fetchall()
            
            if export_format == 'csv':
                df = pd.DataFrame([dict(row) for row in records])
                filename = f'daily_attendance_{month}.csv'
                os.makedirs('static/reports', exist_ok=True)
                df.to_csv(f'static/reports/{filename}', index=False)
                return jsonify({'status': 'success', 'filename': filename})
            
            elif export_format == 'excel':
                df = pd.DataFrame([dict(row) for row in records])
                filename = f'daily_attendance_{month}.xlsx'
                os.makedirs('static/reports', exist_ok=True)
                df.to_excel(f'static/reports/{filename}', index=False)
                return jsonify({'status': 'success', 'filename': filename})
        
        elif report_type == 'monthly':
            # Monthly report
            year, month_num = month.split('-')
            records = conn.execute('''
                SELECT student_id, name, department,
                       COUNT(CASE WHEN date IS NOT NULL THEN 1 END) as total_present,
                       COUNT(*) as total_days
                FROM attendance 
                WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
                GROUP BY student_id
            ''', (year, month_num)).fetchall()
            
            if export_format == 'csv':
                df = pd.DataFrame([dict(row) for row in records])
                filename = f'monthly_attendance_{year}_{month_num}.csv'
                os.makedirs('static/reports', exist_ok=True)
                df.to_csv(f'static/reports/{filename}', index=False)
                return jsonify({'status': 'success', 'filename': filename})
            
            elif export_format == 'excel':
                df = pd.DataFrame([dict(row) for row in records])
                filename = f'monthly_attendance_{year}_{month_num}.xlsx'
                os.makedirs('static/reports', exist_ok=True)
                df.to_excel(f'static/reports/{filename}', index=False)
                return jsonify({'status': 'success', 'filename': filename})
    
    # Get statistics
    total_students = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    total_attendance = conn.execute('SELECT COUNT(*) FROM attendance').fetchone()[0]
    
    # Get unique dates
    unique_dates = conn.execute('SELECT DISTINCT date FROM attendance ORDER BY date DESC').fetchall()
    
    conn.close()
    
    return render_template('reports.html',
                         total_students=total_students,
                         total_attendance=total_attendance,
                         unique_dates=unique_dates)

@app.route('/download_report/<filename>')
@login_required
def download_report(filename):
    """Download a report file"""
    return redirect(url_for('static', filename=f'reports/{filename}'))

@app.route('/print_report', methods=['POST'])
@login_required
def print_report():
    """Generate printable report"""
    report_type = request.form.get('report_type')
    date_param = request.form.get('date')
    
    conn = get_db_connection()
    
    if report_type == 'daily':
        records = conn.execute('SELECT * FROM attendance WHERE date = ?', (date_param,)).fetchall()
        title = f"Daily Attendance Report - {date_param}"
    else:
        year, month = date_param.split('-')
        records = conn.execute('''
            SELECT student_id, name, department,
                   COUNT(*) as present_count
            FROM attendance 
            WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
            GROUP BY student_id
        ''', (year, month)).fetchall()
        title = f"Monthly Attendance Report - {year}-{month}"
    
    conn.close()
    
    # Pass datetime as template variable
    current_datetime = datetime.now()
    
    return render_template('print_report.html',
                         records=records,
                         title=title,
                         report_type=report_type,
                         current_datetime=current_datetime)

# ==================== STUDENT OPTIONAL ROUTES ====================

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    """Student login for viewing own attendance"""
    error = None
    
    if request.method == 'POST':
        student_id = request.form['student_id']
        
        conn = get_db_connection()
        student = conn.execute('SELECT * FROM students WHERE student_id = ?',
                              (student_id,)).fetchone()
        conn.close()
        
        if student:
            session['student_id'] = student['student_id']
            session['student_name'] = student['name']
            return redirect(url_for('student_dashboard'))
        else:
            error = 'Invalid Student ID!'
    
    return render_template('student_login.html', error=error)

@app.route('/student_dashboard')
def student_dashboard():
    """Student personal dashboard"""
    if 'student_id' not in session:
        return redirect(url_for('student_login'))
    
    conn = get_db_connection()
    student_id = session['student_id']
    
    # Get total attendance
    total_days_result = conn.execute('SELECT COUNT(DISTINCT date) FROM attendance').fetchone()[0]
    total_days = total_days_result if total_days_result else 0
    
    present_days_result = conn.execute(
        'SELECT COUNT(DISTINCT date) FROM attendance WHERE student_id = ?',
        (student_id,)
    ).fetchone()[0]
    present_days = present_days_result if present_days_result else 0
    
    # Get recent attendance
    recent = conn.execute('''
        SELECT * FROM attendance WHERE student_id = ? ORDER BY date DESC, time DESC LIMIT 10
    ''', (student_id,)).fetchall()
    
    conn.close()
    
    # Calculate percentage safely (avoid division by zero)
    percentage = round((present_days / total_days * 100), 2) if total_days > 0 else 0.0
    
    # Get current datetime for template
    current_datetime = datetime.now()
    
    return render_template('student_dashboard.html',
                         student_name=session['student_name'],
                         student_id=student_id,
                         total_days=total_days,
                         present_days=present_days,
                         percentage=percentage,
                         current_datetime=current_datetime,
                         recent=recent)

@app.route('/student_logout')
def student_logout():
    """Logout student"""
    session.pop('student_id', None)
    session.pop('student_name', None)
    return redirect(url_for('student_login'))

# ==================== API ROUTES FOR JAVASCRIPT ====================

@app.route('/api/students')
@login_required
def get_students():
    """Get all students as JSON"""
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students ORDER BY name').fetchall()
    conn.close()
    return jsonify([dict(row) for row in students])

@app.route('/api/attendance_today')
@login_required
def get_attendance_today():
    """Get today's attendance summary"""
    conn = get_db_connection()
    today = date.today().strftime('%Y-%m-%d')
    
    total = conn.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    present = conn.execute(
        'SELECT COUNT(DISTINCT student_id) FROM attendance WHERE date = ?',
        (today,)
    ).fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'date': today,
        'total_students': total,
        'present': present,
        'absent': total - present
    })

# ==================== MAIN ENTRY POINT ====================

if __name__ == '__main__':
    # Initialize database
    init_db()
    
    # Create reports directory
    os.makedirs('static/reports', exist_ok=True)
    
    print("="*60)
    print("SMART ATTENDANCE SYSTEM")
    print("="*60)
    print("\n📋 Project Flow for Viva:")
    print("1. Open browser and go to: http://localhost:5000")
    print("2. Login with: admin / admin123")
    print("3. Register students (capture their faces)")
    print("4. Go to 'Take Attendance' and start camera")
    print("5. Faces will be detected and recognized")
    print("6. View and export reports as needed")
    print("\n✅ Server running at http://localhost:5000")
    print("="*60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)


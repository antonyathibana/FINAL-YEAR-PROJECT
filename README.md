# 🎓 Smart Attendance System Using Face Recognition

A comprehensive face recognition-based attendance management system built with Python Flask, OpenCV, and SQLite.

## 📋 Project Overview

This project is designed for final-year engineering students to demonstrate in their viva voce. It provides a complete attendance management solution using face recognition technology.

## 🌟 Features

### Admin Features
- **Secure Login System** - Admin authentication
- **Dashboard** - Real-time attendance statistics
- **Student Registration** - Capture and store student faces
- **Take Attendance** - Real-time face recognition attendance
- **View Records** - Filter and search attendance logs
- **Generate Reports** - Export to CSV/Excel, print reports

### Student Features (Optional)
- **Self Login** - View personal attendance
- **Attendance Percentage** - Track own attendance
- **History** - View attendance records

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Backend | Python Flask |
| Face Recognition | face_recognition (dlib) |
| Computer Vision | OpenCV |
| Database | SQLite |
| Frontend | HTML5, CSS3, JavaScript |
| Styling | Custom CSS with FontAwesome |

## 📁 Project Structure

```
smart-attendance-system/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── static/
│   ├── student_images/    # Stored face images
│   └── reports/           # Generated reports
└── templates/
    ├── login.html         # Admin login
    ├── dashboard.html     # Admin dashboard
    ├── register.html      # Student registration
    ├── attendance.html    # Take attendance
    ├── view_attendance.html # View records
    ├── reports.html       # Reports page
    ├── print_report.html  # Print template
    ├── student_login.html # Student login
    └── student_dashboard.html # Student dashboard
```

## 🚀 Setup Instructions

### Step 1: Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Install System Dependencies

**macOS:**
```bash
brew install cmake dlib
```

**Ubuntu/Debian:**
```bash
sudo apt-get install cmake libsm6 libxext6 libxrender-dev
```

**Windows:**
Download dlib wheels from: https://github.com/ageitgey/face_recognition

### Step 3: Run the Application

```bash
python app.py
```

### Step 4: Access the Application

Open your browser and navigate to:
```
http://localhost:5000
```

## 🔐 Login Credentials

### Admin Login
- **Username:** admin
- **Password:** admin123

## 📖 How to Use (Viva Flow)

### 1. Initial Setup
```
✓ Start the Flask server
✓ Login as admin
✓ Students sit one by one in front of camera
```

### 2. Register Students
```
✓ Go to "Register Student"
✓ Fill student details (ID, Name, Dept, Year, Section)
✓ Click "Start Camera" → "Capture"
✓ Submit to save
```

### 3. Take Attendance
```
✓ Go to "Take Attendance"
✓ Click "Start Camera"
✓ Students face is recognized automatically
✓ Attendance marked with timestamp
✓ Prevents duplicate entries
```

### 4. View Records
```
✓ Go to "View Attendance"
✓ Filter by date/department/section
✓ See all attendance records
```

### 5. Generate Reports
```
✓ Go to "Reports"
✓ Select daily/monthly report
✓ Choose CSV or Excel format
✓ Download or print
```

## 🎯 Key Concepts for Viva

### Face Recognition Process
1. **Face Detection** - Locate faces in image/video frame
2. **Face Encoding** - Convert face to 128-dimensional vector
3. **Face Matching** - Compare encoding with database
4. **Recognition** - Identify person with best match

### Database Tables
```
Users: Admin login credentials
Students: Student information and face image paths
Attendance: Date, time, student tracking
```

### Technical Highlights
- Real-time face detection using HOG (Histogram of Oriented Gradients)
- Face encoding using deep learning model
- Duplicate prevention for same-day attendance
- Responsive UI with mobile support
- CSV/Excel export functionality

## 📊 Database Schema

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    name TEXT,
    role TEXT
);

-- Students Table
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    student_id TEXT UNIQUE,
    name TEXT,
    department TEXT,
    year TEXT,
    section TEXT,
    image_path TEXT
);

-- Attendance Table
CREATE TABLE attendance (
    id INTEGER PRIMARY KEY,
    student_id TEXT,
    name TEXT,
    department TEXT,
    date DATE,
    time TIME,
    status TEXT
);
```

## ⚠️ Troubleshooting

### Camera Access Error
- Ensure no other app is using camera
- Grant camera permissions to browser
- Try using HTTPS for camera access

### Face Recognition Issues
- Ensure good lighting
- Face should be clearly visible
- Don't wear sunglasses or masks

### Installation Issues
- Install CMake before dlib
- Use Python 3.8-3.11 (best compatibility)
- Consider using conda for package management

## 📱 Demo Script for Viva

1. **Introduction** (2 min)
   - Explain project purpose
   - Show architecture diagram
   - Mention technologies used

2. **Live Demo** (5 min)
   - Login as admin
   - Register a new student
   - Show attendance taking
   - View and export reports

3. **Technical Questions** (10 min)
   - How face recognition works
   - Database design
   - Security considerations
   - Performance optimization

4. **Future Enhancements** (3 min)
   - Multi-camera support
   - SMS/Email notifications
   - Mobile app integration
   - Analytics dashboard

## 📝 Requirements.txt

```
flask==3.0.0
opencv-python==4.8.1.78
face-recognition==1.3.0
numpy==1.24.3
pandas==2.0.3
openpyxl==3.1.2
Werkzeug==2.3.7
```

## 🎓 Academic Value

This project demonstrates:
- Python Flask web development
- Computer vision fundamentals
- Database management
- Responsive UI design
- RESTful API concepts
- User authentication
- File handling

## 📄 License

This project is for educational purposes as a final-year engineering project.

## 👨‍💻 Author

**Project Developer:** [Your Name]  
**College:** [Your College Name]  
**Year:** Final Year Engineering

---

**Note:** For best results, use Python 3.8-3.11 and ensure proper lighting for face recognition.


# Smart Attendance System Using Face Recognition

## Final Year Engineering Project

This application provides:
- Admin/Faculty login system
- Student registration with face capture
- Real-time face detection attendance
- Attendance viewing and reporting
- CSV/Excel export functionality

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Open browser and go to: http://localhost:5000

## Login Credentials

- Username: admin
- Password: admin123

## Features

1. **Admin Dashboard** - View statistics (total students, today's attendance)
2. **Student Registration** - Register students with face capture
3. **Take Attendance** - Real-time face detection attendance using webcam
4. **View Attendance** - Filter and search attendance records
5. **Reports** - Generate daily/monthly reports (CSV/Excel export)
6. **Student Login** - Students can view their own attendance

## Project Flow

1. Admin logs in with credentials
2. Admin registers students by capturing their faces
3. For attendance: Start camera, faces are detected
4. System marks attendance with timestamp
5. View and export reports as needed


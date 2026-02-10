@echo off
REM Smart Attendance System - Windows Setup Script
REM Run this as Administrator

echo 🎓 Smart Attendance System - Setup
echo ==================================

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    pause
    exit /b 1
)

echo ✓ Python found

REM Create virtual environment
echo.
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo ⬆️  Upgrading pip...
python -m pip install --upgrade pip

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

REM Create directories
echo.
echo 📁 Creating project directories...
if not exist "static\student_images" mkdir "static\student_images"
if not exist "static\reports" mkdir "static\reports"

REM Initialize database
echo.
echo 🗄️  Initializing database...
python -c "from app import init_db; init_db(); print('✓ Database initialized')"

echo.
echo ==================================
echo ✅ Setup Complete!
echo.
echo To run the application:
echo 1. Activate virtual environment:
echo    venv\Scripts\activate.bat
echo.
echo 2. Start the server:
echo    python app.py
echo.
echo 3. Open browser:
echo    http://localhost:5000
echo.
echo 🔐 Admin Login:
echo    Username: admin
echo    Password: admin123
echo ==================================

pause


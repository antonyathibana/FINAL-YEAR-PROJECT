#!/bin/bash

# Smart Attendance System - Setup Script
# For macOS/Linux

echo "🎓 Smart Attendance System - Setup"
echo "=================================="

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✓ Python found"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install system dependencies for dlib
echo ""
echo "🔧 Installing system dependencies..."

# Detect OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍺 Detected macOS. Installing with Homebrew..."
    if ! command -v brew &> /dev/null; then
        echo "⚠️  Homebrew not found. Please install manually:"
        echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    else
        echo "📦 Installing cmake..."
        brew install cmake
        
        echo "📦 Installing dlib dependencies..."
        brew install dlib || echo "⚠️  dlib installation may require additional steps"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Detected Linux. Installing dependencies..."
    sudo apt-get update
    sudo apt-get install -y cmake libsm6 libxext6 libxrender-dev
else
    echo "⚠️  Detected $OSTYPE. Please install system dependencies manually:"
    echo "   - CMake"
    echo "   - dlib"
    echo "   - OpenCV development files"
fi

# Create directories
echo ""
echo "📁 Creating project directories..."
mkdir -p static/student_images
mkdir -p static/reports

# Initialize database
echo ""
echo "🗄️  Initializing database..."
python3 -c "from app import init_db; init_db(); print('✓ Database initialized')"

echo ""
echo "=================================="
echo "✅ Setup Complete!"
echo ""
echo "To run the application:"
echo "1. Activate virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the server:"
echo "   python app.py"
echo ""
echo "3. Open browser:"
echo "   http://localhost:5000"
echo ""
echo "🔐 Admin Login:"
echo "   Username: admin"
echo "   Password: admin123"
echo "=================================="


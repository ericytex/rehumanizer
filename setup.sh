#!/bin/bash

echo "🚀 Setting up ReHumanizer development environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p uploads
mkdir -p frontend/src/components
mkdir -p frontend/src/lib
mkdir -p backend/app/models
mkdir -p backend/app/utils

# Set up frontend
echo "📦 Setting up frontend..."
cd frontend
if [ ! -f "package.json" ]; then
    echo "❌ Frontend package.json not found. Please check the project structure."
    exit 1
fi

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

cd ..

# Set up backend
echo "🐍 Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
echo "📦 Installing backend dependencies..."
source venv/bin/activate
pip install -r requirements.txt

cd ..

# Create environment files
echo "⚙️ Creating environment files..."

# Frontend .env.local
cat > frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
EOF

# Backend .env
cat > backend/.env << EOF
DATABASE_URL=postgresql://postgres:password@localhost:5432/rehumanizer
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET=your-jwt-secret-change-in-production
DEBUG=True
EOF

echo "✅ Environment files created"

# Start services with Docker Compose
echo "🐳 Starting services with Docker Compose..."
docker-compose up -d postgres redis

echo "⏳ Waiting for services to be ready..."
sleep 10

# Start backend
echo "🚀 Starting backend..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd ..

# Start frontend
echo "🚀 Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!

cd ..

echo "✅ Setup complete!"
echo ""
echo "🌐 Services are running:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📝 Next steps:"
echo "   1. Visit http://localhost:3000 to see the application"
echo "   2. Visit http://localhost:8000/docs to see the API documentation"
echo "   3. Start developing!"
echo ""
echo "🛑 To stop the services, run:"
echo "   pkill -f uvicorn"
echo "   pkill -f 'npm run dev'"
echo "   docker-compose down" 
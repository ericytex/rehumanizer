# ReHumanizer - AI Text Humanizer SaaS

Transform AI-generated text into human-like content with our advanced NLP algorithms.

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ 
- Python 3.9+
- PostgreSQL
- Redis

### Frontend Setup (NextJS)
```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

### Backend Setup (Python FastAPI)
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --reload
```

## 📁 Project Structure

```
rehumanizer2/
├── frontend/                 # NextJS application
│   ├── src/
│   │   ├── app/             # App router pages
│   │   ├── components/      # Reusable components
│   │   ├── lib/            # Utilities and API calls
│   │   └── styles/         # Global styles
│   ├── public/             # Static assets
│   └── package.json
├── backend/                 # Python FastAPI application
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Configuration and security
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Helper functions
│   ├── requirements.txt
│   └── Dockerfile
├── docs/                   # Documentation
├── requirements.md         # Detailed requirements
└── README.md
```

## 🔧 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Backend (.env)
```env
DATABASE_URL=postgresql://user:password@localhost/rehumanizer
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
JWT_SECRET=your-jwt-secret-here
```

## 🛠️ Development

### Database Setup
```sql
-- Create database
CREATE DATABASE rehumanizer;

-- Run migrations (will be created)
-- See backend/app/models/ for schema
```

### API Documentation
Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🚀 Deployment

### Frontend (Vercel)
```bash
# Deploy to Vercel
vercel --prod
```

### Backend (Docker)
```bash
# Build and run with Docker
docker build -t rehumanizer-backend .
docker run -p 8000:8000 rehumanizer-backend
```

## 📊 Features

### MVP Features
- ✅ Text humanization engine
- ✅ User authentication
- ✅ File upload support
- ✅ Usage tracking
- ✅ Responsive design

### Planned Features
- 🔄 Multi-language support
- 🔄 Advanced AI detection bypass
- 🔄 Bulk processing
- 🔄 API access for developers
- 🔄 Mobile app

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@rehumanizer.com
- 💬 Discord: [Join our community](https://discord.gg/rehumanizer)
- 📖 Docs: [Documentation](https://docs.rehumanizer.com)

---

**Built with ❤️ using NextJS and FastAPI** 
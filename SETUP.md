# 🚀 Marie Knowledge System - Setup Guide

## Prerequisites

- **Python 3.9+** (for backend)
- **Node.js 18+** (for frontend)
- **Git** (for version control)
- **Ollama** (for local AI models) - Optional for Phase 1

## Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd marie-knowledge-system
npm install  # Install concurrently for development scripts
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Environment Configuration
Create `.env` file in the root directory:
```env
# Database
DATABASE_URL=sqlite:///./marie.db

# AI Models (Optional for Phase 1)
OLLAMA_BASE_URL=http://localhost:11434
LIGHTWEIGHT_MODEL=llama3.2:3b
DEEP_MODEL=llama3.1:8b

# Security
SECRET_KEY=your-secret-key-change-in-production

# Development
DEBUG=true
```

### 5. Run Development Servers
```bash
# From root directory - runs both backend and frontend
npm run dev

# Or run separately:
npm run dev:backend   # Backend on http://localhost:8000
npm run dev:frontend  # Frontend on http://localhost:5173
```

## Development Workflow

### Phase 1: MVP Development (Current)
Focus on core functionality without AI complexity:

1. **Backend**: Basic CRUD operations for laboratories
2. **Frontend**: Simple React components with Tailwind CSS
3. **Database**: SQLite with basic tables
4. **No AI**: Skip AI features for now, focus on data flow

### Available Scripts
```bash
npm run dev          # Run both backend and frontend
npm run build        # Build both applications
npm run test         # Run all tests
npm run lint         # Lint both codebases
```

### Backend Development
```bash
cd backend
uvicorn app.main:app --reload  # Start backend server
python -m pytest              # Run tests
```

### Frontend Development
```bash
cd frontend
npm run dev    # Start development server
npm run build  # Build for production
npm run test   # Run tests
```

## Project Structure

```
marie/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # API routes
│   │   ├── core/           # Configuration & database
│   │   ├── models/         # SQLAlchemy models
│   │   └── main.py         # FastAPI app
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   └── App.tsx         # Main app
│   └── package.json
├── docs/                   # Documentation
└── README.md
```

## API Endpoints

### Laboratories
- `GET /api/v1/laboratories/` - List all laboratories
- `POST /api/v1/laboratories/` - Create laboratory
- `GET /api/v1/laboratories/{id}` - Get laboratory
- `PUT /api/v1/laboratories/{id}` - Update laboratory
- `DELETE /api/v1/laboratories/{id}` - Delete laboratory

### Health Check
- `GET /health` - Application health status
- `GET /docs` - API documentation (Swagger)

## Database

### Initial Tables (Phase 1)
- `laboratories` - Knowledge domains
- `concepts` - Atomic knowledge units (coming in Phase 2)
- `sources` - Content references (coming in Phase 2)

### Database Commands
```bash
# Reset database (development only)
python -c "from app.core.database import reset_database; reset_database()"
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Change ports in `vite.config.ts` or `main.py`
2. **Python virtual environment**: Ensure it's activated before installing packages
3. **Node modules**: Delete `node_modules` and run `npm install` if issues persist

### Development Tips

1. **Hot reload**: Both backend and frontend support hot reload
2. **API testing**: Use `/docs` endpoint for interactive API testing
3. **Database inspection**: Use SQLite browser to inspect `marie.db`

## Next Steps

1. **Phase 1**: Complete basic laboratory CRUD operations
2. **Phase 2**: Add visual improvements and animations
3. **Phase 3**: Integrate AI models and advanced features
4. **Phase 4**: Polish UI/UX and add premium features

## Contributing

1. Create feature branch: `git checkout -b feature/amazing-feature`
2. Make changes and test locally
3. Commit: `git commit -m 'Add amazing feature'`
4. Push: `git push origin feature/amazing-feature`
5. Create Pull Request

---

*"Nothing in life is to be feared, it is only to be understood."* - Marie Curie

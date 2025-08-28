# 🧪 Marie - Personal Knowledge Management System

> *Inspired by Marie Curie's rigorous methodology and insatiable curiosity*

Marie is an AI-powered personal knowledge management system that integrates Zettelkasten methodology, bidirectional relationships, semantic search, and interactive learning to help you organize, connect, and master diverse information sources.

## 🎯 Vision

Empower continuous learning and innovation by freeing users from repetitive organization tasks, allowing them to focus on insights and knowledge transformation.

## ✨ Key Features

### 🧪 Laboratory System
- **Separate Knowledge Domains**: Independent spaces for different subjects (AI, Philosophy, etc.)
- **Isolated Search**: Each laboratory maintains its own knowledge ecosystem
- **Custom Configuration**: Personalized AI models, sources, and tags per domain

### 🔍 Hybrid Search Engine
- **Semantic Search**: Vector-based similarity using embeddings
- **Keyword Search**: Traditional BM25 ranking with SQLite FTS5
- **Tag-based Filtering**: Flexible categorization system
- **Smart Re-ranking**: Combined scoring for optimal results

### 🧠 Interactive Mind Map
- **Visual Progress Tracking**: Color-coded nodes based on mastery level
- **Smart Recommendations**: AI-suggested next topics based on prerequisites
- **Adaptive Assessments**: Dynamic quizzes that adjust to your level
- **Learning Paths**: Optimized routes through knowledge domains

### 📔 Laboratory Notebook
- **Personal Annotations**: Capture insights while studying
- **Saved Searches**: Bookmark important queries with context
- **Progress Tracking**: Monitor learning velocity and confidence
- **Smart Reminders**: Spaced repetition based on forgetting curve

### 📚 Specialized Source Libraries
- **Academic Integration**: ArXiv, Papers With Code, Google Scholar
- **Book Libraries**: Z-Library integration for free access
- **Course Platforms**: Coursera, edX recommendations
- **One-click Import**: Automatic processing and connection

## 🏗️ Architecture

### Backend
- **FastAPI**: Modern Python web framework
- **SQLite**: Relational data storage
- **Chroma DB**: Vector database for embeddings
- **NetworkX**: Graph relationships
- **Ollama**: Local LLM management

### Frontend
- **React 18 + TypeScript**: Modern component architecture
- **Vite**: Fast development and building
- **Tailwind CSS**: Utility-first styling
- **Framer Motion**: Smooth animations
- **React Flow**: Interactive mind maps
- **D3.js**: Custom visualizations

## 🚀 Development Phases

### Phase 1: MVP Functional (Weeks 1-3)
- [ ] Basic dashboard with laboratory cards
- [ ] Content ingestion system
- [ ] Simple search functionality
- [ ] Basic notebook editor
- [ ] Laboratory management

### Phase 2: Visual Improvements (Weeks 4-6)
- [ ] Enhanced UI with animations
- [ ] Progress bars and visual feedback
- [ ] Icon system and color themes
- [ ] Improved navigation

### Phase 3: Advanced Interactivity (Weeks 7-10)
- [ ] Interactive mind map
- [ ] Advanced search with filters
- [ ] Drag & drop functionality
- [ ] Assessment system

### Phase 4: Premium Experience (Weeks 11-14)
- [ ] Cinematic animations
- [ ] Theme customization
- [ ] Advanced visualizations
- [ ] Mobile responsiveness

## 📁 Project Structure

```
marie/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── hooks/          # Custom hooks
│   │   ├── stores/         # State management
│   │   ├── services/       # API services
│   │   └── types/          # TypeScript types
│   ├── public/             # Static assets
│   └── package.json        # Node dependencies
├── docs/                   # Documentation
│   ├── PRD.md             # Product Requirements
│   ├── sistema-relaciones-busqueda.md
│   └── zettelkasten-metodologia.md
└── README.md              # This file
```

## 🛠️ Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- Git

### Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Access the Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 🧪 Zettelkasten Integration

Marie implements core Zettelkasten principles:
- **Atomicity**: Each concept is a discrete, focused unit
- **Autonomy**: Notes are self-contained and understandable
- **Connectivity**: Bidirectional links between related concepts
- **Reformulation**: AI helps rephrase content in your own words

## 🤖 AI Models

### Lightweight Model (Basic Tasks)
- **Llama-3.2-3B** or **Phi-3-mini**
- Content extraction and basic analysis
- Tag suggestions and categorization

### Deep Model (Complex Analysis)
- **Llama-3.1-8B** or **Mistral-7B**
- Semantic relationship detection
- Advanced summarization and insights

## 📊 Database Schema

Key tables:
- `laboratories`: Knowledge domain separation
- `concepts`: Atomic knowledge units
- `relationships`: Bidirectional connections
- `sources`: Content references with metadata
- `tags`: Flexible categorization system
- `lab_notebook_entries`: Personal annotations
- `topic_assessments`: Learning evaluations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Marie Curie**: For her rigorous scientific methodology and pioneering spirit
- **Niklas Luhmann**: For the Zettelkasten methodology
- **Rubén Loan**: For modern Zettelkasten adaptations
- **Open Source Community**: For the amazing tools that make this possible

---

*"Nothing in life is to be feared, it is only to be understood. Now is the time to understand more, so that we may fear less."* - Marie Curie

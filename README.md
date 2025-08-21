# AI-Powered Cover Letter Generator

An intelligent web application that generates personalized cover letters by analyzing job postings and matching them with your CV/resume.

## 🚀 Features

- **Smart Analysis**: Extract key skills and requirements from job postings using NLP
- **CV Matching**: Automatically match your experience with job requirements
- **AI-Powered Generation**: Create personalized cover letters using OpenAI
- **Multiple Tones**: Choose from formal, friendly, or concise writing styles
- **Export Options**: Download as PDF, DOCX, or TXT
- **Skill Gap Analysis**: Identify missing skills and provide recommendations

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, spaCy, OpenAI API
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Export**: python-docx, reportlab

## 📁 Project Structure

```
AI-Powered_Cover_Letter_Generator/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Core functionality
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic
│   ├── requirements.txt
│   └── main.py
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Utilities
│   │   └── types/         # TypeScript types
│   ├── package.json
│   └── next.config.js
├── README.md
└── .gitignore
```

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## 📝 Development Roadmap

- [x] **Phase 1**: Basic project structure
- [ ] **Phase 2**: NLP pipeline and CV parsing
- [ ] **Phase 3**: AI integration and cover letter generation
- [ ] **Phase 4**: Export functionality and UI polish

## 🤝 Contributing

This is a showcase project demonstrating NLP, LLM, and full-stack web development skills.

## 📄 License

MIT License

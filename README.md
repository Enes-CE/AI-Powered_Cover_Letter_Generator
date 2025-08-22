# 🚀 AI-Powered Cover Letter Generator

Modern, AI-driven cover letter generator with beautiful UI and advanced NLP capabilities.

## ✨ Features

- 🤖 **AI-Powered Generation**: Uses Ollama (Llama 3.1 8B) for high-quality cover letters
- 🎨 **Modern UI**: Dark blue theme with glassmorphism effects
- 📄 **PDF Upload**: Extract text from CV PDFs automatically
- 📊 **Smart Analysis**: AI-powered skill matching and job analysis
- 🔄 **Multi-variant**: Generate multiple cover letter versions
- 📤 **Export Options**: PDF and DOCX export functionality
- 🌍 **Multi-language**: Turkish and English support
- 📱 **Responsive**: Works perfectly on all devices

## 🛠️ Tech Stack

### Frontend
- **Next.js 14** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Lucide React** - Icons

### Backend
- **FastAPI** - Python web framework
- **Ollama** - Local LLM (Llama 3.1 8B)
- **SpaCy** - NLP processing
- **PyPDF2** - PDF text extraction
- **ReportLab** - PDF generation
- **python-docx** - DOCX generation

## 🚀 Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Ollama (for local AI)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/your-username/AI-Powered_Cover_Letter_Generator.git
cd AI-Powered_Cover_Letter_Generator
```

2. **Backend Setup**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

3. **Install Ollama**
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Download Llama 3.1 8B
ollama pull llama3.1:8b
```

4. **Start Backend**
```bash
cd backend
source venv/bin/activate
python -c "import uvicorn; from main import app; uvicorn.run(app, host='0.0.0.0', port=8003)"
```

5. **Frontend Setup**
```bash
cd frontend
npm install
npm run dev
```

6. **Open Application**
- Frontend: http://localhost:3000
- Backend: http://localhost:8003

## 🌐 Deployment

### Frontend (Vercel)

1. **Connect to Vercel**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Vercel will auto-detect Next.js

2. **Environment Variables**
   - Add `NEXT_PUBLIC_API_URL` with your backend URL

3. **Deploy**
   - Vercel will automatically deploy on push to main

### Backend (Railway)

1. **Connect to Railway**
   - Go to [railway.app](https://railway.app)
   - Import your GitHub repository
   - Select the `backend` directory

2. **Environment Variables**
   ```
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3.1:8b
   AI_TIMEOUT=180
   ```

3. **Deploy**
   - Railway will automatically deploy on push to main

### Alternative: Render

1. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository

2. **Configuration**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

## 📝 Usage

1. **Enter Job Posting**: Paste the job description
2. **Add Company Details**: Company name and position
3. **Upload CV**: Either paste text or upload PDF
4. **Choose Options**: Select tone and number of variants
5. **Generate**: Click to create cover letters
6. **Export**: Download as PDF or DOCX

## 🔧 Configuration

### AI Provider Settings
```python
# backend/app/settings.py
AI_PROVIDER = "ollama"  # ollama | openai | template
OLLAMA_MODEL = "llama3.1:8b"
AI_TIMEOUT = 180
```

### Frontend API URL
```typescript
// frontend/src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8003';
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Ollama](https://ollama.ai) for local LLM capabilities
- [SpaCy](https://spacy.io) for NLP processing
- [Next.js](https://nextjs.org) for the frontend framework
- [FastAPI](https://fastapi.tiangolo.com) for the backend framework

## 📞 Support

If you have any questions or need help, please open an issue on GitHub.

---

**Made with ❤️ using AI and modern web technologies**

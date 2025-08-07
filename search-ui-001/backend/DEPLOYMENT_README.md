# Elastic Search Application - Deployment Guide

## 🚀 Quick Start

This application provides a comprehensive search interface with document enrichment capabilities, featuring:
- **Backend API**: FastAPI-based search engine with Elasticsearch integration
- **Frontend**: React-based search interface with real-time filtering
- **Enrichment Framework**: NLP-powered document enrichment with keyword extraction

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+** and npm
- **Elasticsearch 8.x** (accessible at `http://ozdb:9200` or configure in `backend/config.yaml`)
- **Git**

## 🛠️ Installation

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd elastic

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2. Install Python Dependencies

```bash
# Install all Python dependencies
pip install -r requirements.txt

# Install spaCy English model
python -m spacy download en_core_web_sm

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words'); nltk.download('wordnet')"
```

### 3. Install Frontend Dependencies

```bash
# Install Node.js dependencies
cd frontend
npm install
cd ..
```

### 4. Configure Elasticsearch

Edit `backend/config.yaml` to match your Elasticsearch setup:

```yaml
elasticsearch:
  host: "http://your-elasticsearch-host:9200"
  username: "elastic"
  password: "your-password"
  indexes:
    - "your-index-name_enriched"
```

## 🚀 Running the Application

### Development Mode

```bash
# Terminal 1: Start Backend
python run_backend.py

# Terminal 2: Start Frontend
cd frontend && npm start
```

### Production Mode

```bash
# Backend (production)
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend (build and serve)
cd frontend
npm run build
# Serve the build folder with your preferred web server
```

## 📁 Project Structure

```
elastic/
├── backend/                 # FastAPI backend
│   ├── app.py              # Main API endpoints
│   ├── config.yaml         # Backend configuration
│   └── main.py             # Application entry point
├── enrichment/             # Document enrichment framework
│   ├── cli.py              # Command-line interface
│   ├── core.py             # Core enrichment logic
│   ├── config.yaml         # Enrichment configuration
│   └── verification/       # Test and verification scripts
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom React hooks
│   │   └── styles/         # CSS styles
│   └── package.json        # Frontend dependencies
├── venv/                   # Python virtual environment
├── requirements.txt        # Python dependencies
├── run_backend.py          # Backend runner script
├── run_enrichment.py       # Enrichment runner script
└── README.md               # This file
```

## 🔧 Configuration

### Backend Configuration (`backend/config.yaml`)

```yaml
elasticsearch:
  host: "http://ozdb:9200"
  username: "elastic"
  password: ""
  indexes:
    - "semantic-python-index_enriched"
    - "semantic-elastic-co-index_enriched"
    - "semantic-wikipedia-index_enriched"

content_paths:
  clean_content: "content.body.clean_content"
  raw_html: "content.body.raw_html"
  title: "title.raw"
  description: "description.raw"
  url: "url.raw"

common:
  api_key: "xyz123"
```

### Enrichment Configuration (`enrichment/config.yaml`)

```yaml
elasticsearch:
  host: "http://ozdb:9200"
  username: "elastic"
  password: ""

indexes:
  semantic-python-index: semantic-python-index_enriched
  semantic-elastic-co-index: semantic-elastic-co-index_enriched
  semantic-wikipedia-index: semantic-wikipedia-index_enriched

content_paths:
  clean_content: "content.body.clean_content"
  raw_html: "content.body.raw_html"
  title: "title.raw"
  description: "description.raw"
  url: "url.raw"
```

## 🔍 Using the Enrichment Framework

### Basic Commands

```bash
# Show help
python run_enrichment.py --help

# Check source indexes
python run_enrichment.py check-sources

# Enrich documents
python run_enrichment.py enrich

# Verify enrichment
python run_enrichment.py verify

# Delete enriched indexes
python run_enrichment.py delete-enriched
```

### Advanced Usage

```bash
# Extract keywords only
python run_enrichment.py extract

# Run verification tests
python run_verification.py
```

## 🌐 API Endpoints

### Search API

- `GET /api/elasticsearch/search` - Main search endpoint
- `GET /health` - Health check
- `GET /` - Root endpoint

### Example Search Request

```bash
curl "http://localhost:8000/api/elasticsearch/search?q=python&api_key=xyz123&search_type=semantic&size=10"
```

## 🔒 Security

- API key authentication is required for all search endpoints
- Default API key: `xyz123` (change in `backend/config.yaml`)
- Elasticsearch authentication can be configured in the config files

## 🐛 Troubleshooting

### Common Issues

1. **Elasticsearch Connection Error**
   - Verify Elasticsearch is running
   - Check host/port in config files
   - Ensure authentication credentials are correct

2. **NLP Model Errors**
   - Run: `python -m spacy download en_core_web_sm`
   - Download NLTK data as shown in installation

3. **Frontend Build Errors**
   - Clear node_modules: `rm -rf frontend/node_modules && npm install`
   - Check Node.js version compatibility

4. **Import Errors**
   - Ensure virtual environment is activated
   - Verify all dependencies are installed

### Logs

- Backend logs: Check terminal output when running `python run_backend.py`
- Frontend logs: Check browser console and terminal output
- Enrichment logs: Check output when running enrichment commands

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the logs for error messages
3. Verify all prerequisites are met
4. Contact the development team

## 🔄 Updates

To update the application:

```bash
# Pull latest changes
git pull origin main

# Update Python dependencies
pip install -r requirements.txt --upgrade

# Update frontend dependencies
cd frontend && npm install && cd ..

# Restart the application
```

---

**Version**: 1.0.0  
**Last Updated**: December 2024  
**Maintainer**: Development Team 
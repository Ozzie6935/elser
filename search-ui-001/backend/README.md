# Elasticsearch FastAPI Application

A FastAPI application for searching Elasticsearch using ELSER (semantic), fuzzy, or keyword search.

## Setup

### 1. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Make sure virtual environment is activated
pip install -r requirements.txt
```

### 3. Run the Application

```bash
# Development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or for production
uvicorn main:app --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /api/elasticsearch/search` - Search Elasticsearch documents
- `GET /api/elasticsearch/suggest` - Get search suggestions

## Configuration

The application uses a `config.yaml` file for configuration. You can modify the values in this file to match your environment:

### Elasticsearch Configuration
- `host`: Elasticsearch server URL
- `username`: Elasticsearch username
- `password`: Elasticsearch password
- `ca_cert`: Path to CA certificate file
- `cert_bundle`: Path to certificate bundle file
- `indexes`: List of Elasticsearch indexes to search

### API Configuration
- `api_key`: API key for authentication (default: xyz123)
- `origins`: Allowed CORS origins

### MongoDB Configuration (if needed)
- `connection`: MongoDB connection string
- `username`: MongoDB username
- `password`: MongoDB password
- `database`: MongoDB database name

The application will fall back to environment variables if the config file is not found.

## Deactivate Virtual Environment

When you're done working:

```bash
deactivate
``` 
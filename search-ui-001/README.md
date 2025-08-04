# Elasticsearch Document Enrichment Framework

A comprehensive framework for enriching Elasticsearch documents with intelligent keyword extraction, entity recognition, and metadata analysis.

## 🏗️ Project Structure

```
elastic/
├── backend/                 # FastAPI backend application
│   ├── app.py              # Main API endpoints
│   └── config.yaml         # Backend configuration (enriched indexes only)
├── enrichment/             # Isolated enrichment framework
│   ├── core.py             # Core enrichment operations
│   ├── cli.py              # Command-line interface
│   ├── keyword_extractor.py
│   ├── document_enricher.py
│   ├── enrich_documents.py  # Legacy enrichment entry point
│   ├── config.yaml         # Enrichment configuration (source→enriched mapping)
│   ├── verification/       # Verification and testing scripts
│   │   ├── test_enriched_config.py
│   │   ├── test_content_paths.py
│   │   ├── test_backend_enriched.py
│   │   ├── test_enrichment.py
│   │   ├── verify_enriched_fields.py
│   │   └── ... (other verification scripts)
│   └── requirements.txt    # Enrichment dependencies
├── frontend/               # React frontend application
├── venv/                   # Shared Python virtual environment
├── run_backend.py          # Backend runner script
├── run_enrichment.py       # Enrichment runner script (from root)
└── run_verification.py     # Verification runner script (from root)
```

## ⚙️ Configuration

### Backend Configuration (`backend/config.yaml`)

The backend uses a simple list of enriched indexes:

```yaml
common:
  api_key: xyz123
  origins: http://localhost:3000

elasticsearch:
  host: http://ozdb:9200
  username: 
  password: 
  verify: false
  ca_cert: 
  cert_bundle: 
  indexes:
     - semantic-python-index_enriched
     - semantic-elastic-co-index_enriched
     - semantic-wikipedia-index_enriched

content_paths:
  # Configurable paths to content fields
  clean_content: content.body.clean_content
  raw_html: content.body.raw_html
  title: title.raw
  description: description.raw
  url: url.raw
```

### Enrichment Configuration (`enrichment/config.yaml`)

The enrichment framework uses source→enriched index mapping:

```yaml
common:
  api_key: xyz123
  origins: http://localhost:3000

elasticsearch:
  host: http://ozdb:9200
  username: 
  password: 
  verify: false
  ca_cert: 
  cert_bundle: 
  indexes:
     semantic-python-index: semantic-python-index_enriched
     semantic-elastic-co-index: semantic-elastic-co-index_enriched
     semantic-wikipedia-index: semantic-wikipedia-index_enriched

content_paths:
  # Configurable paths to content fields
  clean_content: content.body.clean_content
  raw_html: content.body.raw_html
  title: title.raw
  description: description.raw
  url: url.raw
```

## 🔧 Content Path Configuration

The `content_paths` section allows you to customize how the framework accesses content fields in your Elasticsearch documents. This is especially useful when deploying to different environments with different document structures.

### Default Paths
- `clean_content`: `content.body.clean_content`
- `raw_html`: `content.body.raw_html`
- `title`: `title.raw`
- `description`: `description.raw`
- `url`: `url.raw`

### Custom Paths Example
If your documents have a different structure, you can customize the paths:

```yaml
content_paths:
  clean_content: text.clean
  raw_html: text.html
  title: page.title
  description: page.description
  url: link
```

## 🚀 Usage

### 1. Setup Virtual Environment
```bash
# Activate the shared virtual environment
source venv/bin/activate
```

### 2. Quick Start
```bash
# Show help and available commands
python3 run_enrichment.py

# Create new enriched indexes (recommended)
python3 run_enrichment.py enrich --create-new
```

### 3. Run Enrichment Process


**Using the Modular CLI (Recommended):**
```bash
# Show help (default behavior)
python3 run_enrichment.py

# Create new enriched indexes
python3 run_enrichment.py enrich --create-new

# Update existing documents
python3 run_enrichment.py enrich --update-existing

# Process specific indexes
python3 run_enrichment.py enrich --create-new --indexes semantic-python-index

# Dry run (see what would be done)
python3 run_enrichment.py enrich --create-new --dry-run
```

**Using the Legacy Script:**
```bash
# From enrichment directory
cd enrichment
../venv/bin/python enrich_documents.py
```

### 4. Available Commands

**Enrichment:**
```bash
# Create new enriched indexes
python3 run_enrichment.py enrich --create-new

# Update existing documents
python3 run_enrichment.py enrich --update-existing

# Process specific indexes with custom batch size
python3 run_enrichment.py enrich --create-new --indexes semantic-python-index --batch-size 50

# Dry run to see what would be done
python3 run_enrichment.py enrich --create-new --dry-run
```

**Verification:**
```bash
# Verify enriched indexes
python3 run_enrichment.py verify

# Check source indexes
python3 run_enrichment.py check-sources

# Delete enriched indexes
python3 run_enrichment.py delete-enriched --confirm
```

**Keyword Extraction:**
```bash
# Extract keywords only
python3 run_enrichment.py extract --index semantic-python-index --output keywords.json
```

### 4. Start Backend
```bash
# From project root
python3 run_backend.py

# Or from backend directory
cd backend
../venv/bin/uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 5. Start Frontend
```bash
cd frontend
npm start
```

## 📊 Enriched Fields

The enrichment process adds the following fields to your documents:

- **`programming_language`**: Extracted programming languages (Python, Java, Go, etc.)
- **`framework`**: Frameworks and libraries (Django, React, etc.)
- **`tool`**: Development tools (Docker, Kubernetes, AWS, etc.)
- **`concept`**: Technical concepts (AI, Machine Learning, API, etc.)
- **`technical_terms`**: All technical keywords and terms
- **`entities`**: Named entities (persons, organizations, locations, etc.)
- **`content_type`**: Content type classification
- **`domain`**: Domain information
- **`content_length`**: Content length categorization
- **`language`**: Document language

## 🔍 Testing

### Test Content Paths
```bash
cd enrichment
../venv/bin/python verification/test_content_paths.py
```

### Test Backend with Enriched Indexes
```bash
cd enrichment
../venv/bin/python verification/test_backend_enriched.py
```

### Test Enrichment Process
```bash
cd enrichment
../venv/bin/python verification/test_enrichment.py
```

## 🏗️ Modular Architecture

The enrichment framework is built with a modular architecture for better maintainability and extensibility:

### Core Components

- **`core.py`**: Central enrichment operations and utilities
- **`cli.py`**: Command-line interface with argparse
- **`keyword_extractor.py`**: Smart keyword extraction logic
- **`document_enricher.py`**: Document enrichment orchestration

### CLI Commands

The framework provides a comprehensive CLI with the following commands:

- **`enrich`**: Enrich documents with keywords and metadata
- **`extract`**: Extract keywords from documents
- **`verify`**: Verify enriched indexes
- **`check-sources`**: Check source indexes
- **`delete-enriched`**: Delete enriched indexes

### Usage Patterns

```python
# Programmatic usage
from core import create_enrichment_core

core = create_enrichment_core("config.yaml")
results = core.create_enriched_indexes(batch_size=100)
```

## 🛠️ Customization

### Adding New Content Paths
1. Update the `content_paths` section in both config files
2. The framework will automatically use the new paths

### Adding New Indexes
1. **For Enrichment**: Add source→enriched mapping to `enrichment/config.yaml`
2. **For Backend**: Add enriched index name to `backend/config.yaml`

### Customizing Keyword Extraction
Modify the technical patterns in `keyword_extractor.py`:
- Programming languages
- Frameworks and libraries
- Development tools
- Technical concepts

### Extending the CLI
Add new commands by:
1. Adding a new subparser in `cli.py`
2. Creating a command handler function
3. Adding the handler to the `command_handlers` dictionary

## 📝 Notes

- The enrichment framework is completely isolated and self-contained
- The backend only needs to know about enriched indexes
- Content paths are configurable for different document structures
- All scripts use the shared virtual environment at the project root
- The framework supports both create-new-index and update-existing modes 
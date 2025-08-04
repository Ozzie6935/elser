# Smart Keyword Extraction System

This system provides intelligent keyword extraction from Elasticsearch documents to enhance search aggregations and filtering capabilities.

## 🚀 Features

- **Intelligent Keyword Extraction**: Uses NLP techniques to extract meaningful keywords
- **Technical Term Recognition**: Identifies programming languages, frameworks, tools, and concepts
- **Named Entity Recognition**: Extracts people, organizations, locations, and other entities
- **URL Pattern Analysis**: Categorizes content based on URL patterns
- **Multi-Index Processing**: Processes all three indexes (Python, Elastic, Wikipedia)
- **Enhanced Aggregations**: Creates new Elasticsearch fields for better filtering

## 📋 Prerequisites

- Python 3.8+
- Elasticsearch running with your indexes
- Access to the indexes via API

## 🛠️ Installation

### 1. Install Required Packages

```bash
# Install basic requirements
pip install -r requirements_keywords.txt

# Or run the setup script
python setup_nlp.py
```

### 2. Download NLP Models

```bash
# Download spaCy English model
python -m spacy download en_core_web_sm

# Download NLTK data (handled by setup script)
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger'); nltk.download('maxent_ne_chunker'); nltk.download('words'); nltk.download('wordnet')"
```

## 🔧 Usage

### Step 1: Extract Keywords

```bash
cd backend
python keyword_extractor.py
```

This will:
- Process all documents from the three indexes
- Extract technical keywords, entities, and metadata
- Generate `keywords_library.json` with all extracted keywords
- Generate `aggregation_suggestions.json` with Elasticsearch aggregation recommendations

### Step 2: Update Elasticsearch Mapping

```bash
python update_mapping.py
```

This will add new keyword fields to your indexes for enhanced aggregations.

### Step 3: Update Backend Aggregations

Update your `app.py` to include the new aggregation fields:

```python
"aggs": {
    "source": {"terms": {"field": "_index"}},
    "programming_language": {"terms": {"field": "programming_language.keyword"}},
    "framework": {"terms": {"field": "framework.keyword"}},
    "tool": {"terms": {"field": "tool.keyword"}},
    "concept": {"terms": {"field": "concept.keyword"}},
    "content_type": {"terms": {"field": "content_type.keyword"}},
    "domain": {"terms": {"field": "domain.keyword"}},
    "technical_terms": {"terms": {"field": "technical_terms.keyword", "size": 50}},
    "entities_person": {"terms": {"field": "entities.person.keyword"}},
    "entities_organization": {"terms": {"field": "entities.organization.keyword"}},
    "content_length": {"terms": {"field": "content_length.keyword"}}
}
```

## 📊 Output Files

### keywords_library.json
Contains all extracted keywords organized by category:

```json
{
  "technical_terms": ["python", "elasticsearch", "api", "rest", "..."],
  "programming_languages": ["python", "javascript", "java", "..."],
  "frameworks": ["django", "flask", "react", "..."],
  "tools": ["git", "docker", "kubernetes", "..."],
  "concepts": ["api", "rest", "microservices", "..."],
  "domains": ["python.org", "elastic.co", "wikipedia.org"],
  "content_types": ["guide", "reference", "api", "wiki", "..."],
  "entities": {
    "person": ["John Doe", "..."],
    "organization": ["Python Software Foundation", "..."],
    "location": ["San Francisco", "..."]
  },
  "index_stats": {
    "semantic-python-index": 9,
    "semantic-elastic-co-index": 5,
    "semantic-wikipedia-index": 4
  }
}
```

### aggregation_suggestions.json
Contains recommendations for Elasticsearch aggregations:

```json
{
  "field_aggregations": {
    "programming_language": {
      "type": "terms",
      "field": "programming_language.keyword",
      "size": 20
    }
  },
  "script_aggregations": {
    "technical_terms_count": {
      "type": "cardinality",
      "script": {
        "source": "return doc['content.body.clean_content'].value.split().length"
      }
    }
  },
  "recommendations": [
    "Add programming_language, framework, tool fields to document mapping",
    "Implement content_type field based on URL patterns",
    "Add technical_terms field for advanced filtering"
  ]
}
```

## 🔍 Keyword Extraction Methods

### 1. Technical Term Recognition
- **Programming Languages**: Python, JavaScript, Java, C++, etc.
- **Frameworks**: Django, Flask, React, Angular, etc.
- **Tools**: Git, Docker, Kubernetes, AWS, etc.
- **Concepts**: API, REST, Microservices, DevOps, etc.

### 2. NLP-Based Extraction
- **Part-of-Speech Tagging**: Identifies nouns, adjectives, technical terms
- **Named Entity Recognition**: Extracts people, organizations, locations
- **Lemmatization**: Normalizes words to their base form
- **Stop Word Removal**: Filters out common words

### 3. URL Pattern Analysis
- **Content Type**: guide, reference, api, wiki, tutorial, blog
- **Domain**: python.org, elastic.co, wikipedia.org
- **Section**: python, elastic, wikipedia

### 4. Content Analysis
- **Code Patterns**: Function calls, class definitions, import statements
- **Technical Patterns**: API endpoints, configuration patterns
- **Document Structure**: Headers, lists, code blocks

## 🎯 Enhanced Filtering Options

After running the keyword extraction, you'll have access to these new filtering options:

### Programming Languages
- Python, JavaScript, Java, C++, C#, PHP, Ruby, Go, Rust, etc.

### Frameworks
- Django, Flask, FastAPI, React, Angular, Vue, Express, Spring, etc.

### Tools
- Git, Docker, Kubernetes, AWS, Azure, GCP, MySQL, PostgreSQL, etc.

### Concepts
- API, REST, GraphQL, Microservices, Serverless, DevOps, CI/CD, etc.

### Content Types
- Guide, Reference, API, Wiki, Tutorial, Blog, Documentation

### Entities
- People, Organizations, Locations, Products, Events

## 🔧 Customization

### Adding New Technical Terms

Edit the `_init_technical_patterns()` method in `keyword_extractor.py`:

```python
def _init_technical_patterns(self):
    self.programming_languages.update(['new_language'])
    self.frameworks.update(['new_framework'])
    self.tools.update(['new_tool'])
    self.concepts.update(['new_concept'])
```

### Custom URL Patterns

Modify the `extract_url_metadata()` method to add new URL patterns:

```python
if '/custom/' in path:
    metadata['content_type'] = 'custom'
```

### Custom Entity Types

Add new entity types in the mapping and extraction logic:

```python
# In update_mapping.py
"custom_entity": {
    "type": "keyword",
    "fields": {
        "text": {"type": "text"}
    }
}
```

## 🚨 Troubleshooting

### Common Issues

1. **NLTK Data Not Found**
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```

2. **spaCy Model Not Found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

3. **Elasticsearch Connection Error**
   - Check your `config.yaml` file
   - Verify Elasticsearch is running
   - Check API key permissions

4. **Memory Issues with Large Datasets**
   - Reduce batch size in `extract_documents_from_index()`
   - Process indexes separately
   - Use streaming for very large datasets

### Performance Optimization

- **Batch Processing**: Adjust `batch_size` in document extraction
- **Parallel Processing**: Use multiprocessing for large datasets
- **Caching**: Cache extracted keywords to avoid reprocessing
- **Incremental Updates**: Only process new documents

## 📈 Future Enhancements

1. **Machine Learning Integration**
   - Train custom models for domain-specific keyword extraction
   - Use embeddings for semantic keyword clustering

2. **Real-time Processing**
   - Stream processing for new documents
   - Incremental keyword updates

3. **Advanced Analytics**
   - Keyword frequency analysis
   - Trend detection over time
   - Content similarity scoring

4. **Multi-language Support**
   - Support for non-English content
   - Language-specific keyword extraction

## 🤝 Contributing

To contribute to the keyword extraction system:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License. 
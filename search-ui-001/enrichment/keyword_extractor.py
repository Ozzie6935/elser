#!/usr/bin/env python3
"""
Smart Keyword Extractor for Elasticsearch Documents
Extracts intelligent keywords and metadata from document content for enhanced filtering
"""

import json
import re
import requests
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple
import logging
from urllib.parse import urlparse
import yaml

# NLP libraries for intelligent keyword extraction
NLTK_AVAILABLE = False
SPACY_AVAILABLE = False

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.stem import WordNetLemmatizer, PorterStemmer
    from nltk.tag import pos_tag
    from nltk.chunk import ne_chunk
    NLTK_AVAILABLE = True
except ImportError:
    print("NLTK not available. Install with: pip install nltk")

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    print("spaCy not available. Install with: pip install spacy")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SmartKeywordExtractor:
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the keyword extractor with configuration"""
        self.config = self._load_config(config_path)
        self.es_url = self.config['elasticsearch']['host']
        self.api_key = self.config['common']['api_key']
        
        # Initialize NLP components
        self._init_nlp()
        
        # Keywords storage
        self.keywords_library = {
            'technical_terms': set(),
            'programming_languages': set(),
            'frameworks': set(),
            'tools': set(),
            'concepts': set(),
            'domains': set(),
            'content_types': set(),
            'url_patterns': set(),
            'entities': defaultdict(set)
        }
        
        # Common technical terms and patterns
        self._init_technical_patterns()
    
    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Config file {config_path} not found")
            raise
    
    def _get_content_by_path(self, doc: Dict, path: str) -> str:
        """Get content from document using dot-notation path"""
        try:
            keys = path.split('.')
            value = doc
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key, '')
                else:
                    return str(value) if value else ''
            return str(value) if value else ''
        except Exception as e:
            logger.warning(f"Error accessing path {path}: {e}")
            return ''
    
    def _init_nlp(self):
        """Initialize NLP components"""
        global NLTK_AVAILABLE, SPACY_AVAILABLE
        if NLTK_AVAILABLE:
            try:
                # Download required NLTK data
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('averaged_perceptron_tagger', quiet=True)
                nltk.download('maxent_ne_chunker', quiet=True)
                nltk.download('words', quiet=True)
                nltk.download('wordnet', quiet=True)
                
                self.stop_words = set(stopwords.words('english'))
                self.lemmatizer = WordNetLemmatizer()
                self.stemmer = PorterStemmer()
                logger.info("NLTK components initialized successfully")
            except Exception as e:
                logger.warning(f"Failed to initialize NLTK: {e}")
                NLTK_AVAILABLE = False
        
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load("en_core_web_sm")
                logger.info("spaCy model loaded successfully")
            except OSError:
                logger.warning("spaCy model not found. Install with: python -m spacy download en_core_web_sm")
                SPACY_AVAILABLE = False
    
    def _init_technical_patterns(self):
        """Initialize technical term patterns"""
        self.programming_languages = {
            'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'bash', 'shell',
            'typescript', 'dart', 'elixir', 'clojure', 'haskell', 'erlang'
        }
        
        self.frameworks = {
            'django', 'flask', 'fastapi', 'react', 'angular', 'vue', 'express', 
            'spring', 'laravel', 'rails', 'asp.net', 'node.js', 'jquery',
            'bootstrap', 'tailwind', 'material-ui', 'tensorflow', 'pytorch'
        }
        
        self.tools = {
            'git', 'docker', 'kubernetes', 'jenkins', 'travis', 'github', 'gitlab',
            'aws', 'azure', 'gcp', 'heroku', 'elasticsearch', 'kibana', 'logstash',
            'mysql', 'postgresql', 'mongodb', 'redis', 'nginx', 'apache'
        }
        
        self.concepts = {
            'api', 'rest', 'graphql', 'microservices', 'serverless', 'devops',
            'ci/cd', 'agile', 'scrum', 'tdd', 'bdd', 'ddd', 'mvp', 'poc',
            'machine learning', 'ai', 'deep learning', 'nlp', 'computer vision'
        }
    
    def extract_documents_from_index(self, index_name: str, batch_size: int = 1000) -> List[Dict]:
        """Extract documents from a specific index"""
        url = f"{self.es_url}/{index_name}/_search"
        headers = {"Content-Type": "application/json"}
        
        # Query to get all documents
        query = {
            "size": batch_size,  # Use the provided batch_size parameter
            "query": {
                "match_all": {}
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=query, verify=False)
            response.raise_for_status()
            data = response.json()
            
            hits = data.get('hits', {}).get('hits', [])
            documents = []
            
            for hit in hits:
                source = hit.get('_source', {})
                doc_id = hit.get('_id')
                
                # Extract content from the document
                content_body = source.get('content', {}).get('body', {})
                clean_content = content_body.get('clean_content', '')
                raw_html = content_body.get('raw_html', '')
                
                if clean_content or raw_html:
                    documents.append({
                        'id': doc_id,
                        **source  # Spread the original source document
                    })
            
            logger.info(f"📄 Found {len(documents)} documents in {index_name}")
            return documents
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error extracting documents from {index_name}: {e}")
            return []
    
    def extract_url_metadata(self, url: str) -> Dict:
        """Extract metadata from URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            metadata = {
                'domain': domain,
                'path': path,
                'content_type': 'other',
                'section': 'other'
            }
            
            # Determine content type from URL
            if '/guide/' in path:
                metadata['content_type'] = 'guide'
            elif '/reference/' in path:
                metadata['content_type'] = 'reference'
            elif '/api/' in path:
                metadata['content_type'] = 'api'
            elif '/docs/' in path:
                metadata['content_type'] = 'documentation'
            elif '/wiki/' in path or 'wikipedia.org' in domain:
                metadata['content_type'] = 'wiki'
            elif '/tutorial/' in path:
                metadata['content_type'] = 'tutorial'
            elif '/blog/' in path:
                metadata['content_type'] = 'blog'
            
            # Determine section from domain
            if 'python.org' in domain:
                metadata['section'] = 'python'
            elif 'elastic.co' in domain:
                metadata['section'] = 'elastic'
            elif 'wikipedia.org' in domain:
                metadata['section'] = 'wikipedia'
            
            return metadata
        except Exception as e:
            logger.warning(f"Error parsing URL {url}: {e}")
            return {'domain': 'unknown', 'path': '', 'content_type': 'other', 'section': 'other'}
    
    def extract_technical_keywords(self, text: str) -> Set[str]:
        """Extract technical keywords using multiple approaches"""
        keywords = set()
        
        if not text:
            return keywords
        
        # Convert to lowercase for matching
        text_lower = text.lower()
        
        # Extract programming languages
        for lang in self.programming_languages:
            if lang in text_lower:
                keywords.add(lang)
        
        # Extract frameworks
        for framework in self.frameworks:
            if framework in text_lower:
                keywords.add(framework)
        
        # Extract tools
        for tool in self.tools:
            if tool in text_lower:
                keywords.add(tool)
        
        # Extract concepts
        for concept in self.concepts:
            if concept in text_lower:
                keywords.add(concept)
        
        # Extract code patterns (functions, classes, etc.)
        code_patterns = [
            r'\b[A-Z][a-zA-Z]*\(\)',  # Function calls like Python()
            r'\b[A-Z][a-zA-Z]*\.[a-zA-Z_]+\(\)',  # Method calls like Class.method()
            r'\bimport\s+[a-zA-Z_]+',  # Import statements
            r'\bfrom\s+[a-zA-Z_.]+\s+import',  # From imports
            r'\bclass\s+[A-Z][a-zA-Z]*',  # Class definitions
            r'\bdef\s+[a-zA-Z_]+',  # Function definitions
        ]
        
        for pattern in code_patterns:
            matches = re.findall(pattern, text)
            keywords.update(matches)
        
        return keywords
    
    def extract_nlp_keywords(self, text: str) -> Set[str]:
        """Extract keywords using NLP techniques"""
        keywords = set()
        
        if not text or not NLTK_AVAILABLE:
            return keywords
        
        try:
            # Tokenize and tag parts of speech
            tokens = word_tokenize(text.lower())
            pos_tags = pos_tag(tokens)
            
            # Extract nouns, adjectives, and technical terms
            for word, tag in pos_tags:
                if (tag.startswith('NN') or tag.startswith('JJ')) and len(word) > 2:
                    # Lemmatize the word
                    lemma = self.lemmatizer.lemmatize(word)
                    if lemma not in self.stop_words:
                        keywords.add(lemma)
            
            # Named Entity Recognition
            named_entities = ne_chunk(pos_tags)
            for chunk in named_entities:
                if hasattr(chunk, 'label'):
                    entity_text = ' '.join([token for token, pos in chunk.leaves()])
                    keywords.add(entity_text.lower())
        
        except Exception as e:
            logger.warning(f"Error in NLP keyword extraction: {e}")
        
        return keywords
    
    def extract_spacy_entities(self, text: str) -> Dict[str, Set[str]]:
        """Extract entities using spaCy"""
        entities = defaultdict(set)
        
        if not text or not SPACY_AVAILABLE:
            return entities
        
        try:
            doc = self.nlp(text)
            
            for ent in doc.ents:
                entity_type = ent.label_.lower()
                entity_text = ent.text.lower().strip()
                if len(entity_text) > 2:
                    entities[entity_type].add(entity_text)
        
        except Exception as e:
            logger.warning(f"Error in spaCy entity extraction: {e}")
        
        return entities
    
    def extract_keywords_from_document(self, doc: Dict) -> Dict:
        """Extract keywords from a single document"""
        keywords = {
            'technical_terms': set(),
            'programming_languages': set(),
            'frameworks': set(),
            'tools': set(),
            'concepts': set(),
            'entities': defaultdict(set),
            'url_metadata': {}
        }
        
        # Get content paths from config
        content_paths = self.config.get('content_paths', {})
        
        # Combine all text content using configurable paths
        clean_content = self._get_content_by_path(doc, content_paths.get('clean_content', 'content.body.clean_content'))
        raw_html = self._get_content_by_path(doc, content_paths.get('raw_html', 'content.body.raw_html'))
        title = self._get_content_by_path(doc, content_paths.get('title', 'title.raw'))
        description = self._get_content_by_path(doc, content_paths.get('description', 'description.raw'))
        
        all_text = f"{title} {description} {clean_content}"
        
        # Extract URL metadata using configurable path
        url = self._get_content_by_path(doc, content_paths.get('url', 'url.raw'))
        if url:
            keywords['url_metadata'] = self.extract_url_metadata(url)
        
        # Extract technical keywords
        keywords['technical_terms'] = self.extract_technical_keywords(all_text)
        
        # Extract programming languages, frameworks, tools, concepts
        keywords['programming_languages'] = keywords['technical_terms'] & self.programming_languages
        keywords['frameworks'] = keywords['technical_terms'] & self.frameworks
        keywords['tools'] = keywords['technical_terms'] & self.tools
        keywords['concepts'] = keywords['technical_terms'] & self.concepts
        
        # Extract NLP keywords
        nlp_keywords = self.extract_nlp_keywords(all_text)
        keywords['technical_terms'].update(nlp_keywords)
        
        # Extract spaCy entities
        spacy_entities = self.extract_spacy_entities(all_text)
        for entity_type, entity_set in spacy_entities.items():
            keywords['entities'][entity_type].update(entity_set)
        
        return keywords
    
    def process_all_indexes(self) -> Dict:
        """Process all indexes and extract keywords"""
        indexes = ['semantic-python-index', 'semantic-elastic-co-index', 'semantic-wikipedia-index']
        
        all_keywords = {
            'technical_terms': set(),
            'programming_languages': set(),
            'frameworks': set(),
            'tools': set(),
            'concepts': set(),
            'domains': set(),
            'content_types': set(),
            'entities': defaultdict(set),
            'index_stats': {}
        }
        
        for index_name in indexes:
            logger.info(f"Processing index: {index_name}")
            
            # Extract documents
            documents = self.extract_documents_from_index(index_name)
            all_keywords['index_stats'][index_name] = len(documents)
            
            # Process each document
            for doc in documents:
                doc_keywords = self.extract_keywords_from_document(doc)
                
                # Aggregate keywords
                all_keywords['technical_terms'].update(doc_keywords['technical_terms'])
                all_keywords['programming_languages'].update(doc_keywords['programming_languages'])
                all_keywords['frameworks'].update(doc_keywords['frameworks'])
                all_keywords['tools'].update(doc_keywords['tools'])
                all_keywords['concepts'].update(doc_keywords['concepts'])
                
                # Aggregate entities
                for entity_type, entity_set in doc_keywords['entities'].items():
                    all_keywords['entities'][entity_type].update(entity_set)
                
                # Aggregate URL metadata
                url_metadata = doc_keywords.get('url_metadata', {})
                if url_metadata.get('domain'):
                    all_keywords['domains'].add(url_metadata['domain'])
                if url_metadata.get('content_type'):
                    all_keywords['content_types'].add(url_metadata['content_type'])
        
        return all_keywords
    
    def save_keywords_library(self, keywords: Dict, output_file: str = "keywords_library.json"):
        """Save the keywords library to a JSON file"""
        # Convert sets to lists for JSON serialization
        serializable_keywords = {}
        for key, value in keywords.items():
            if isinstance(value, set):
                serializable_keywords[key] = sorted(list(value))
            elif isinstance(value, defaultdict):
                serializable_keywords[key] = {
                    k: sorted(list(v)) for k, v in value.items()
                }
            else:
                serializable_keywords[key] = value
        
        with open(output_file, 'w') as f:
            json.dump(serializable_keywords, f, indent=2)
        
        logger.info(f"Keywords library saved to {output_file}")
    
    def generate_aggregation_suggestions(self, keywords: Dict) -> Dict:
        """Generate suggestions for Elasticsearch aggregations"""
        suggestions = {
            'field_aggregations': {},
            'script_aggregations': {},
            'recommendations': []
        }
        
        # Field-based aggregations
        if keywords['programming_languages']:
            suggestions['field_aggregations']['programming_language'] = {
                'type': 'terms',
                'field': 'programming_language.keyword',
                'size': 20
            }
        
        if keywords['frameworks']:
            suggestions['field_aggregations']['framework'] = {
                'type': 'terms',
                'field': 'framework.keyword',
                'size': 20
            }
        
        if keywords['tools']:
            suggestions['field_aggregations']['tool'] = {
                'type': 'terms',
                'field': 'tool.keyword',
                'size': 20
            }
        
        if keywords['content_types']:
            suggestions['field_aggregations']['content_type'] = {
                'type': 'terms',
                'field': 'content_type.keyword',
                'size': 10
            }
        
        # Script-based aggregations for content analysis
        suggestions['script_aggregations'] = {
            'technical_terms_count': {
                'type': 'cardinality',
                'script': {
                    'source': 'return doc["content.body.clean_content"].value.split().length'
                }
            }
        }
        
        # Recommendations
        suggestions['recommendations'] = [
            "Add programming_language, framework, tool fields to document mapping",
            "Implement content_type field based on URL patterns",
            "Add technical_terms field for advanced filtering",
            "Consider adding entity extraction fields (person, organization, location)",
            "Implement content length categorization (short, medium, long)"
        ]
        
        return suggestions

def main():
    """Main function to run the keyword extraction"""
    try:
        # Initialize extractor
        extractor = SmartKeywordExtractor()
        
        # Process all indexes
        logger.info("Starting keyword extraction from all indexes...")
        keywords = extractor.process_all_indexes()
        
        # Save keywords library
        extractor.save_keywords_library(keywords)
        
        # Generate aggregation suggestions
        suggestions = extractor.generate_aggregation_suggestions(keywords)
        
        # Save suggestions
        with open("aggregation_suggestions.json", 'w') as f:
            json.dump(suggestions, f, indent=2)
        
        # Print summary
        print("\n" + "="*50)
        print("KEYWORD EXTRACTION SUMMARY")
        print("="*50)
        print(f"Documents processed: {sum(keywords['index_stats'].values())}")
        print(f"Technical terms found: {len(keywords['technical_terms'])}")
        print(f"Programming languages: {len(keywords['programming_languages'])}")
        print(f"Frameworks: {len(keywords['frameworks'])}")
        print(f"Tools: {len(keywords['tools'])}")
        print(f"Concepts: {len(keywords['concepts'])}")
        print(f"Content types: {len(keywords['content_types'])}")
        print(f"Domains: {len(keywords['domains'])}")
        print(f"Entity types: {len(keywords['entities'])}")
        
        print("\nTop technical terms:")
        for term in sorted(keywords['technical_terms'])[:20]:
            print(f"  - {term}")
        
        print("\nFiles generated:")
        print("  - keywords_library.json")
        print("  - aggregation_suggestions.json")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Detailed verification script to examine document content and keyword extraction
"""

import requests
import json
import yaml
from typing import Dict, List

def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def examine_document_content():
    """Examine the actual content of documents to understand keyword extraction"""
    config = load_config()
    es_url = config['elasticsearch']['host']
    headers = {'Content-Type': 'application/json'}
    
    print("🔍 Detailed Document Content Examination")
    print("=" * 70)
    
    # Check one document from each index
    indexes = ['semantic-python-index_enriched', 'semantic-elastic-co-index_enriched', 'semantic-wikipedia-index_enriched']
    
    for index in indexes:
        print(f'\n📋 Examining: {index}')
        print('-' * 60)
        
        try:
            # Get one document
            url = f'{es_url}/{index}/_search'
            query = {'size': 1, 'query': {'match_all': {}}}
            
            response = requests.post(url, headers=headers, json=query, verify=False)
            response.raise_for_status()
            
            data = response.json()
            hits = data.get('hits', {}).get('hits', [])
            
            if hits:
                doc = hits[0]['_source']
                doc_id = hits[0]['_id']
                
                print(f'📄 Document ID: {doc_id}')
                
                # Examine content fields
                content = doc.get('content', {})
                body = content.get('body', {})
                clean_content = body.get('clean_content', '')
                raw_html = body.get('raw_html', '')
                
                print(f'\n📝 Content Analysis:')
                print(f'  Clean content length: {len(clean_content)} characters')
                print(f'  Raw HTML length: {len(raw_html)} characters')
                
                if clean_content:
                    print(f'  Clean content preview: {clean_content[:200]}...')
                elif raw_html:
                    print(f'  Raw HTML preview: {raw_html[:200]}...')
                else:
                    print('  ⚠️  No content found!')
                
                # Check URL
                url_info = doc.get('url', {})
                raw_url = url_info.get('raw', '')
                print(f'\n🔗 URL: {raw_url}')
                
                # Check title and description
                title = doc.get('title', {}).get('raw', '')
                description = doc.get('description', {}).get('raw', '')
                
                print(f'\n📋 Title: {title}')
                print(f'📄 Description: {description}')
                
                # Show enriched fields
                print(f'\n✨ Enriched Fields:')
                enriched_fields = ['programming_language', 'framework', 'tool', 'concept', 'content_type', 'domain', 'technical_terms', 'entities', 'content_length', 'language']
                
                for field in enriched_fields:
                    value = doc.get(field, 'NOT_FOUND')
                    if isinstance(value, list):
                        print(f'  {field}: {len(value)} items - {value}')
                    elif isinstance(value, dict):
                        print(f'  {field}: {len(value)} keys - {list(value.keys())}')
                    else:
                        print(f'  {field}: {value}')
                
            else:
                print('❌ No documents found')
                
        except Exception as e:
            print(f'❌ Error examining {index}: {e}')

def check_original_vs_enriched():
    """Compare original documents with enriched ones"""
    config = load_config()
    es_url = config['elasticsearch']['host']
    headers = {'Content-Type': 'application/json'}
    
    print("\n🔄 Original vs Enriched Comparison")
    print("=" * 70)
    
    # Compare one document from each pair
    comparisons = [
        ('semantic-python-index', 'semantic-python-index_enriched'),
        ('semantic-elastic-co-index', 'semantic-elastic-co-index_enriched'),
        ('semantic-wikipedia-index', 'semantic-wikipedia-index_enriched')
    ]
    
    for original, enriched in comparisons:
        print(f'\n📊 Comparing: {original} → {enriched}')
        print('-' * 50)
        
        try:
            # Get one document from each
            for index_name in [original, enriched]:
                url = f'{es_url}/{index_name}/_search'
                query = {'size': 1, 'query': {'match_all': {}}}
                
                response = requests.post(url, headers=headers, json=query, verify=False)
                response.raise_for_status()
                
                data = response.json()
                hits = data.get('hits', {}).get('hits', [])
                
                if hits:
                    doc = hits[0]['_source']
                    print(f'  📄 {index_name}: {len(doc)} fields')
                    
                    # Show field count difference
                    if index_name == enriched:
                        original_fields = set(doc.keys()) - {'programming_language', 'framework', 'tool', 'concept', 'content_type', 'domain', 'technical_terms', 'entities', 'content_length', 'language'}
                        enriched_fields = set(doc.keys())
                        new_fields = enriched_fields - original_fields
                        print(f'  ✨ New fields added: {len(new_fields)}')
                        print(f'  📈 Field increase: {len(enriched_fields) - len(original_fields)}')
                else:
                    print(f'  ❌ No documents in {index_name}')
                    
        except Exception as e:
            print(f'❌ Error comparing {original} vs {enriched}: {e}')

def test_keyword_extraction():
    """Test the keyword extraction on sample content"""
    print("\n🧪 Testing Keyword Extraction")
    print("=" * 70)
    
    # Sample content that should trigger keyword extraction
    sample_content = """
    Python is a programming language that supports multiple programming paradigms.
    Django and Flask are popular web frameworks for Python.
    Elasticsearch is a distributed search engine built on Apache Lucene.
    We use Docker for containerization and Kubernetes for orchestration.
    Machine learning and artificial intelligence are key concepts in modern software.
    """
    
    print(f"📝 Sample content: {sample_content.strip()}")
    
    # Import and test the keyword extractor
    try:
        from keyword_extractor import SmartKeywordExtractor
        
        extractor = SmartKeywordExtractor()
        
        # Test technical keyword extraction
        technical_keywords = extractor.extract_technical_keywords(sample_content)
        print(f"\n🔧 Technical keywords found: {technical_keywords}")
        
        # Test URL metadata extraction
        test_url = "https://docs.python.org/3/tutorial/"
        url_metadata = extractor.extract_url_metadata(test_url)
        print(f"\n🔗 URL metadata for {test_url}: {url_metadata}")
        
    except Exception as e:
        print(f"❌ Error testing keyword extraction: {e}")

if __name__ == "__main__":
    examine_document_content()
    check_original_vs_enriched()
    test_keyword_extraction() 
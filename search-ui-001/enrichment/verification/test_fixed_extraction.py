#!/usr/bin/env python3
"""
Test the fixed keyword extraction with actual document structure
"""

import requests
import json
import yaml
from keyword_extractor import SmartKeywordExtractor

def load_config(config_path: str = "config.yaml") -> dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def test_keyword_extraction():
    """Test keyword extraction with a real document"""
    config = load_config()
    es_url = config['elasticsearch']['host']
    headers = {'Content-Type': 'application/json'}
    
    print("🧪 Testing Fixed Keyword Extraction")
    print("=" * 50)
    
    # Get one document from the original index
    index_name = 'semantic-wikipedia-index'
    url = f'{es_url}/{index_name}/_search'
    query = {'size': 1, 'query': {'match_all': {}}}
    
    try:
        response = requests.post(url, headers=headers, json=query, verify=False)
        response.raise_for_status()
        
        data = response.json()
        hits = data.get('hits', {}).get('hits', [])
        
        if hits:
            doc = hits[0]['_source']
            doc_id = hits[0]['_id']
            
            print(f"📄 Testing with document ID: {doc_id}")
            
            # Test the keyword extraction
            extractor = SmartKeywordExtractor()
            keywords = extractor.extract_keywords_from_document(doc)
            
            print(f"\n🔧 Extracted Keywords:")
            print(f"  Technical terms: {len(keywords['technical_terms'])} items")
            if keywords['technical_terms']:
                print(f"    Sample: {list(keywords['technical_terms'])[:10]}")
            
            print(f"  Programming languages: {len(keywords['programming_languages'])} items")
            if keywords['programming_languages']:
                print(f"    Found: {list(keywords['programming_languages'])}")
            
            print(f"  Frameworks: {len(keywords['frameworks'])} items")
            if keywords['frameworks']:
                print(f"    Found: {list(keywords['frameworks'])}")
            
            print(f"  Tools: {len(keywords['tools'])} items")
            if keywords['tools']:
                print(f"    Found: {list(keywords['tools'])}")
            
            print(f"  Concepts: {len(keywords['concepts'])} items")
            if keywords['concepts']:
                print(f"    Found: {list(keywords['concepts'])}")
            
            print(f"  URL metadata: {keywords['url_metadata']}")
            
            print(f"  Entities: {len(keywords['entities'])} types")
            for entity_type, entities in keywords['entities'].items():
                if entities:
                    print(f"    {entity_type}: {list(entities)[:5]}")
            
            # Test content length calculation
            content_body = doc.get('content', {}).get('body', {})
            clean_content = content_body.get('clean_content', '')
            content_length = len(clean_content)
            print(f"\n📏 Content length: {content_length} characters")
            
            if content_length < 1000:
                length_category = 'short'
            elif content_length < 5000:
                length_category = 'medium'
            else:
                length_category = 'long'
            print(f"📊 Length category: {length_category}")
            
            return True
            
        else:
            print("❌ No documents found")
            return False
            
    except Exception as e:
        print(f"❌ Error testing keyword extraction: {e}")
        return False

if __name__ == "__main__":
    test_keyword_extraction() 
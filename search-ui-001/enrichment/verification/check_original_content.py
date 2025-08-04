#!/usr/bin/env python3
"""
Check the original document structure to understand content storage
"""

import requests
import json
import yaml
from typing import Dict, List

def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def examine_original_documents():
    """Examine original documents to understand their structure"""
    config = load_config()
    es_url = config['elasticsearch']['host']
    headers = {'Content-Type': 'application/json'}
    
    print("🔍 Examining Original Document Structure")
    print("=" * 70)
    
    # Check original indexes
    indexes = ['semantic-python-index', 'semantic-elastic-co-index', 'semantic-wikipedia-index']
    
    for index in indexes:
        print(f'\n📋 Examining original index: {index}')
        print('-' * 60)
        
        try:
            # Get multiple documents to see patterns
            url = f'{es_url}/{index}/_search'
            query = {'size': 3, 'query': {'match_all': {}}}
            
            response = requests.post(url, headers=headers, json=query, verify=False)
            response.raise_for_status()
            
            data = response.json()
            hits = data.get('hits', {}).get('hits', [])
            
            print(f'📄 Found {len(hits)} documents to examine')
            
            for i, hit in enumerate(hits):
                doc = hit['_source']
                doc_id = hit['_id']
                
                print(f'\n  📄 Document {i+1} - ID: {doc_id}')
                print(f'  📊 Total fields: {len(doc)}')
                print(f'  🔑 Field names: {list(doc.keys())}')
                
                # Check for content in various possible locations
                content_locations = [
                    'content',
                    'content.body',
                    'content.body.clean_content',
                    'content.body.raw_html',
                    'body',
                    'text',
                    'html',
                    'raw_content',
                    'clean_content'
                ]
                
                print(f'  📝 Content check:')
                for location in content_locations:
                    try:
                        # Navigate nested structure
                        value = doc
                        for key in location.split('.'):
                            if isinstance(value, dict) and key in value:
                                value = value[key]
                            else:
                                value = None
                                break
                        
                        if value and isinstance(value, str) and len(value.strip()) > 0:
                            print(f'    ✅ {location}: {len(value)} chars - "{value[:100]}..."')
                        elif value:
                            print(f'    ⚠️  {location}: {type(value)} - {value}')
                        else:
                            print(f'    ❌ {location}: Not found or empty')
                    except Exception as e:
                        print(f'    ❌ {location}: Error - {e}')
                
                # Check URL and metadata
                url_info = doc.get('url', {})
                if isinstance(url_info, dict):
                    raw_url = url_info.get('raw', '')
                else:
                    raw_url = str(url_info)
                
                print(f'  🔗 URL: {raw_url}')
                
                # Check title and description
                title = doc.get('title', {})
                if isinstance(title, dict):
                    title = title.get('raw', '')
                description = doc.get('description', {})
                if isinstance(description, dict):
                    description = description.get('raw', '')
                
                print(f'  📋 Title: {title}')
                print(f'  📄 Description: {description}')
                
                # Show a few sample field values
                print(f'  🔍 Sample field values:')
                for key, value in list(doc.items())[:5]:
                    if isinstance(value, str) and len(value) > 0:
                        print(f'    {key}: "{value[:50]}..."')
                    elif isinstance(value, (list, dict)):
                        print(f'    {key}: {type(value)} with {len(value)} items')
                    else:
                        print(f'    {key}: {value}')
                
                print('  ' + '-' * 40)
                
        except Exception as e:
            print(f'❌ Error examining {index}: {e}')

def check_document_count():
    """Check document counts in all indexes"""
    config = load_config()
    es_url = config['elasticsearch']['host']
    headers = {'Content-Type': 'application/json'}
    
    print("\n📊 Document Counts")
    print("=" * 70)
    
    all_indexes = [
        'semantic-python-index', 'semantic-python-index_enriched',
        'semantic-elastic-co-index', 'semantic-elastic-co-index_enriched',
        'semantic-wikipedia-index', 'semantic-wikipedia-index_enriched'
    ]
    
    for index in all_indexes:
        try:
            url = f'{es_url}/{index}/_count'
            response = requests.post(url, headers=headers, json={'query': {'match_all': {}}}, verify=False)
            response.raise_for_status()
            
            count = response.json().get('count', 0)
            print(f'📈 {index}: {count} documents')
            
        except Exception as e:
            print(f'❌ Error getting count for {index}: {e}')

if __name__ == "__main__":
    examine_original_documents()
    check_document_count() 
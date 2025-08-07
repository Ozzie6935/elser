#!/usr/bin/env python3
"""
Script to verify that enriched fields were properly added to documents
"""

import requests
import json
import yaml
from typing import Dict, List

def load_config(config_path: str = "config.yaml") -> Dict:
    """Load configuration from YAML file"""
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def verify_enriched_fields():
    """Verify that enriched fields were added to documents"""
    # Load configuration
    config = load_config()
    es_url = config['elasticsearch']['host']
    headers = {'Content-Type': 'application/json'}
    
    # Check one document from each enriched index
    indexes = ['semantic-python-index_enriched', 'semantic-elastic-co-index_enriched', 'semantic-wikipedia-index_enriched']
    
    print("🔍 Verifying Enriched Fields")
    print("=" * 60)
    
    for index in indexes:
        print(f'\n📋 Checking index: {index}')
        print('-' * 50)
        
        try:
            # Get one document to see the structure
            url = f'{es_url}/{index}/_search'
            query = {'size': 1, 'query': {'match_all': {}}}
            
            response = requests.post(url, headers=headers, json=query, verify=False)
            response.raise_for_status()
            
            data = response.json()
            hits = data.get('hits', {}).get('hits', [])
            
            if hits:
                doc = hits[0]['_source']
                print(f'📄 Document ID: {hits[0]["_id"]}')
                print(f'📊 Total fields: {len(doc)}')
                
                # Show the new enriched fields
                enriched_fields = [
                    'programming_language', 'framework', 'tool', 'concept', 
                    'content_type', 'domain', 'technical_terms', 'entities', 
                    'content_length', 'language'
                ]
                
                print('\n✨ Enriched fields found:')
                found_fields = 0
                for field in enriched_fields:
                    if field in doc:
                        value = doc[field]
                        found_fields += 1
                        if isinstance(value, list) and len(value) > 0:
                            print(f'  ✅ {field}: {len(value)} items - {value[:3]}...')
                        elif isinstance(value, dict) and value:
                            print(f'  ✅ {field}: {len(value)} entity types')
                        else:
                            print(f'  ✅ {field}: {value}')
                    else:
                        print(f'  ❌ {field}: Not found')
                
                print(f'\n📈 Enrichment success rate: {found_fields}/{len(enriched_fields)} fields ({found_fields/len(enriched_fields)*100:.1f}%)')
                
                # Show sample of technical terms
                if 'technical_terms' in doc and doc['technical_terms']:
                    print(f'\n🔧 Sample technical terms: {doc["technical_terms"][:10]}')
                
                # Show entities if available
                if 'entities' in doc and doc['entities']:
                    print(f'\n🏷️  Entity types found: {list(doc["entities"].keys())}')
                    for entity_type, entities in doc['entities'].items():
                        if entities:
                            print(f'  - {entity_type}: {entities[:3]}...')
                
            else:
                print('❌ No documents found in this index')
                
        except Exception as e:
            print(f'❌ Error checking {index}: {e}')
    
    print("\n" + "=" * 60)
    print("🎯 Verification Complete!")

def check_index_stats():
    """Check statistics for each enriched index"""
    config = load_config()
    es_url = config['elasticsearch']['host']
    headers = {'Content-Type': 'application/json'}
    
    print("\n📊 Index Statistics")
    print("=" * 60)
    
    indexes = ['semantic-python-index_enriched', 'semantic-elastic-co-index_enriched', 'semantic-wikipedia-index_enriched']
    
    for index in indexes:
        try:
            url = f'{es_url}/{index}/_count'
            response = requests.post(url, headers=headers, json={'query': {'match_all': {}}}, verify=False)
            response.raise_for_status()
            
            count = response.json().get('count', 0)
            print(f'📈 {index}: {count} documents')
            
        except Exception as e:
            print(f'❌ Error getting count for {index}: {e}')

if __name__ == "__main__":
    verify_enriched_fields()
    check_index_stats() 
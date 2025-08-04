#!/usr/bin/env python3
"""
Test script to verify backend works with enriched indexes
"""

import requests
import json
import yaml
import os

def test_backend_with_enriched_indexes():
    """Test that the backend can search enriched indexes"""
    print("🧪 Testing Backend with Enriched Indexes")
    print("=" * 50)
    print()
    
    # Load config
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'backend', 'config.yaml')
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    es_host = config['elasticsearch']['host']
    indexes = config['elasticsearch']['indexes']
    
    print(f"📋 Backend configuration:")
    print(f"  Elasticsearch host: {es_host}")
    print(f"  Indexes: {indexes}")
    print()
    
    # Test basic connectivity to enriched indexes
    headers = {'Content-Type': 'application/json'}
    
    for index in indexes:
        print(f"🔍 Testing index: {index}")
        try:
            # Test count
            count_url = f'{es_host}/{index}/_count'
            count_response = requests.post(count_url, headers=headers, json={'query': {'match_all': {}}}, verify=False)
            count_response.raise_for_status()
            
            doc_count = count_response.json().get('count', 0)
            print(f"  ✅ Connected - {doc_count} documents")
            
            # Test enriched fields
            if doc_count > 0:
                search_url = f'{es_host}/{index}/_search'
                search_query = {
                    'size': 1,
                    'query': {'match_all': {}},
                    '_source': ['programming_language', 'framework', 'tool', 'concept', 'technical_terms']
                }
                
                search_response = requests.post(search_url, headers=headers, json=search_query, verify=False)
                search_response.raise_for_status()
                
                data = search_response.json()
                hits = data.get('hits', {}).get('hits', [])
                
                if hits:
                    doc = hits[0]['_source']
                    enriched_fields = 0
                    for field in ['programming_language', 'framework', 'tool', 'concept', 'technical_terms']:
                        if field in doc and doc[field]:
                            enriched_fields += 1
                    
                    print(f"  ✅ Enriched fields present: {enriched_fields}/5 fields")
                else:
                    print(f"  ⚠️  No documents found in search results")
            else:
                print(f"  ⚠️  No documents in index")
            
            print()
            
        except Exception as e:
            print(f"  ❌ Error testing {index}: {e}")
            print()
    
    print("✅ Backend enriched index testing completed!")

if __name__ == "__main__":
    test_backend_with_enriched_indexes() 